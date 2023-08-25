import gymnasium as gym

import torch

import torch.nn
import torch.optim
from ignite.contrib.engines import common
from ignite.engine import Engine

from ignite.engine.events import Events

from ignite.utils import setup_logger

from tensordict.nn import TensorDictModule

from torchrl.collectors import SyncDataCollector
from torchrl.data import CompositeSpec

from torchrl.data.tensor_specs import DiscreteBox
from torchrl.envs import (
    EnvCreator,
    ExplorationType,
    ObservationNorm,
    ParallelEnv,
    StepCounter,
    ToTensorImage,
    TransformedEnv,
)

from torchrl.envs.libs.gym import GymWrapper
from torchrl.modules import ActorValueOperator, ConvNet, MLP, OneHotCategorical, ProbabilisticActor, ValueOperator
from torchrl.objectives import A2CLoss
from torchrl.objectives.value import GAE
from torchrl.objectives.value.advantages import GAE

# from torchrl.trainers.helpers.envs import get_norm_state_dict

from utils import *


def make_base_env(config):
    env_kwargs = {"id": "CarRacing-v2", "continuous": False, "render_mode": "rgb_array"}

    env = gym.make(**env_kwargs)

    if config.render:

        def trigger_recording(episode):
            return episode % config.save_every_episodes == 0

        env = gym.wrappers.RecordVideo(env, config.recordings_path, episode_trigger=trigger_recording, video_length=0)

    env_kwargs2 = {
        "device": config.device,
        "from_pixels": True,
        "pixels_only": True,
    }

    env = GymWrapper(env, **env_kwargs2)
    print("Base Env Created")
    return env


def get_stats(config):
    env = make_transformed_env_pixels(make_base_env(config), config)
    return get_norm_state_dict(env)


def make_transformed_env_pixels(base_env, config):
    env = TransformedEnv(base_env)
    env.append_transform(ToTensorImage())
    env.append_transform(StepCounter())

    return env


def make_parallel_env(config, state_dict):
    num_envs = config.num_envs
    env = make_transformed_env_pixels(ParallelEnv(num_envs, EnvCreator(lambda: make_base_env(config))), config)
    for t in env.transform:
        if isinstance(t, ObservationNorm):
            t.init_stats(3, cat_dim=1, reduce_dim=[0, 1])
    env.load_state_dict(state_dict, strict=False)
    return env


def make_a2c_models(config):
    base_env = make_transformed_env_pixels(make_base_env(config), config)

    common_module, policy_module, value_module = make_a2c_models_pixels(base_env, config)

    actor_critic = ActorValueOperator(
        common_operator=common_module,
        policy_operator=policy_module,
        value_operator=value_module,
    )

    actor = actor_critic.get_policy_operator()
    critic = actor_critic.get_value_head()  # to avoid

    with torch.no_grad():
        td = base_env.rollout(max_steps=100, break_when_any_done=False)
        td = actor(td)
        td = critic(td)
        del td

    return actor, critic


def make_a2c_models_pixels(base_env, config):
    env = base_env

    # define the input shape
    input_shape = env.observation_spec["pixels"].shape

    # defining the distribution class and kwargs, in this case, the action space is DiscreteBox
    if isinstance(env.action_spec.space, DiscreteBox):
        num_outputs = env.action_spec.space.n
        distribution_class = OneHotCategorical
        distribution_kwargs = {}

    # Define the input keys
    in_keys = ["pixels"]

    # Define a shared Module and TensorDictModule (CNN + MLP)
    common_cnn = ConvNet(
        activation_class=torch.nn.ReLU,
        num_cells=[32, 64, 64],
        kernel_sizes=[3, 1, 1],
        strides=[2, 2, 1],
        device=config.device,
    )
    common_cnn_output = common_cnn(torch.ones(input_shape).to(config.device))
    common_mlp = MLP(
        in_features=common_cnn_output.shape[-1],
        activation_class=torch.nn.ReLU,
        activate_last_layer=True,
        out_features=512,
        num_cells=[],
        device=config.device,
    )
    common_mlp_output = common_mlp(common_cnn_output).to(config.device)

    # Define shared net as TensorDictModule
    common_module = TensorDictModule(
        module=torch.nn.Sequential(common_cnn, common_mlp),
        in_keys=in_keys,
        out_keys=["common_features"],
    )

    # Define on head for the policy
    policy_net = MLP(
        in_features=common_mlp_output.shape[-1],
        out_features=num_outputs,
        num_cells=[256],
        device=config.device,
    )
    policy_module = TensorDictModule(
        module=policy_net,
        in_keys=["common_features"],
        out_keys=["logits"],
    )

    # Add probabilistic sampling of the actions
    policy_module = ProbabilisticActor(
        policy_module,
        in_keys=["logits"],
        spec=CompositeSpec(action=env.action_spec),
        safe=True,
        distribution_class=distribution_class,
        distribution_kwargs=distribution_kwargs,
        return_log_prob=True,
        default_interaction_type=ExplorationType.RANDOM,
    )

    # Define another head for the value
    value_net = MLP(
        in_features=common_mlp_output.shape[-1],
        out_features=1,
        num_cells=[256],
        device=config.device,
    )
    value_module = ValueOperator(
        value_net,
        in_keys=["common_features"],
    )

    return common_module, policy_module, value_module


def make_collector(config, policy):
    collector_class = SyncDataCollector
    state_dict = get_stats(config)
    collector = collector_class(
        make_parallel_env(config, state_dict),
        policy=policy,
        frames_per_batch=config.frames_per_batch,
        total_frames=config.total_frames,
        device=config.device,
        max_frames_per_traj=config.max_frames_per_traj,
    )
    return collector


def make_advantage_module(config, value_network):
    advantage_module = GAE(
        gamma=config.gamma,
        lmbda=config.gae_lambda,
        value_network=value_network,
        average_gae=True,
    )
    return advantage_module


def make_test_env(config):
    num_envs = 1
    state_dict = get_stats(config)
    env = make_parallel_env(config, state_dict)
    return env


def make_loss(config, actor_network, value_network):
    advantage_module = make_advantage_module(config, value_network)
    loss_module = A2CLoss(
        actor=actor_network,
        critic=value_network,
        loss_critic_type=config.loss_critic_type,
        entropy_coef=config.entropy_coef,
        critic_coef=config.critic_coef,
        entropy_bonus=True,
    )
    loss_module.make_value_estimator(gamma=config.gamma)
    return loss_module, advantage_module


def make_optim(config, actor_network, value_network):
    optim = torch.optim.Adam(
        list(actor_network.parameters()) + list(value_network.parameters()),
        lr=config.lr,
        weight_decay=config.weight_decay,
    )
    return optim


def get_norm_state_dict(env):
    """Gets the normalization loc and scale from the env state_dict."""
    sd = env.state_dict()
    sd = {key: val for key, val in sd.items() if key.endswith("loc") or key.endswith("scale")}
    return sd
