from collections import deque, namedtuple

from shutil import copy

import ignite.distributed as idist
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

from ignite.engine import Engine, Events

from ignite.utils import manual_seed

from torch.distributions import Categorical

from utils import *

from typing import Any

import numpy as np

# from matplotlib import pyplot as plt

try:
    import gymnasium as gym
except ImportError:
    raise ModuleNotFoundError("Please install opengym: pip install gymnasium[box2d]")

SavedAction = namedtuple("SavedAction", ["log_prob", "value"])

eps = np.finfo(np.float32).eps.item()


class ActorCriticNetwork(nn.Module):
    def __init__(self, n_actions):
        super(ActorCriticNetwork, self).__init__()
        self.LeakyReLU = nn.LeakyReLU()
        self.Sigmoid = nn.Sigmoid()
        self.Softplus = nn.Softplus()

        # REVIEW:
        # OPTIMIZE:
        self.conv1 = nn.Conv2d(3, 8, kernel_size=7, stride=4, padding=0)
        self.conv2 = nn.Conv2d(8, 16, kernel_size=3, stride=1, padding=2)
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)

        self.fc1 = nn.Linear(576, 512)
        self.fc_critic2 = nn.Linear(512, 1)
        self.fc_actor2 = nn.Linear(512, 256)
        self.fc_actor3 = nn.Linear(256, n_actions)

        self.flatten = nn.Flatten()

        self.saved_actions = []
        self.rewards = []
        self.saved_log_probs = []

    def forward(self, observation):
        # state = torch.Tensor(observation).to(self.device)

        # Shared weights
        x = self.LeakyReLU(self.conv1(observation))
        x = self.pool(x)
        x = self.LeakyReLU(self.conv2(x))
        x = self.pool(x)
        x = self.flatten(x)
        x = self.fc1(x)

        # actor and critic
        # actor
        dist = self.LeakyReLU(self.fc_actor2(x))
        dist = self.Softplus(self.fc_actor3(dist))

        actor = F.softmax(dist, dim=1)

        # critic
        critic = self.fc_critic2(x)

        return actor, critic


# choose an action for the discrete actions
def choose_action(policy, observation):
    observation = observation.float().unsqueeze(0)
    state = torch.transpose(observation, 1, 3)
    probabilities, value = policy(state)
    # probabilities = F.softmax(probabilities)

    action_probs = Categorical(probabilities)
    action = action_probs.sample()

    log_probs = action_probs.log_prob(action)
    policy.saved_actions.append(SavedAction(log_probs, value))
    policy.saved_log_probs.append(log_probs)

    return action.item()


def learn(policy, optimizer, gamma):
    R = 0
    saved_actions = policy.saved_actions
    policy_losses = []  # list to save actor (policy) loss
    value_losses = []  # list to save critic (value) loss
    returns = deque()  # list to save the true values

    for r in policy.rewards[::-1]:
        # calculate the discounted value
        R = r + gamma * R
        returns.appendleft(R)

    returns = torch.tensor(returns)
    returns = (returns - returns.mean()) / (returns.std() + eps)

    for (log_prob, value), R in zip(saved_actions, returns):
        advantage = R - value.item()

        # calculate actor (policy) loss
        policy_losses.append(-log_prob * advantage)

        # calculate critic (value) loss using L1 smooth loss
        value_losses.append(F.smooth_l1_loss(value, torch.tensor([R])))

    # reset gradients
    optimizer.zero_grad()

    # sum up all the values of policy_losses and value_losses
    loss = torch.stack(policy_losses).sum() + torch.stack(value_losses).sum()

    # perform backprop
    loss.backward()
    optimizer.step()
    # reset rewards and action buffer
    del policy.rewards[:]
    del policy.saved_actions[:]


EPISODE_STARTED = Events.EPOCH_STARTED
EPISODE_COMPLETED = Events.EPOCH_COMPLETED


def run(local_rank: int, env: Any, config: Any):
    # make seed
    rank = idist.get_rank()
    manual_seed(config.seed + rank)

    # create output folder and copy config file to ouput dir
    config.output_dir = setup_output_dir(config, rank)
    if rank == 0:
        copy(config.config, f"{config.output_dir}/config-lock.yaml")

    # create wrapper for saving video
    if config.render:

        def trigger(episode):
            return episode % config.save_every_episodes == 0

        env = gym.wrappers.RecordVideo(env, config.recordings_path, trigger)

    # device, policy, optimizer
    device = idist.device()
    actor_critic = ActorCriticNetwork(env.action_space.n).to(device)
    optimizer = idist.auto_optim(optim.Adam(actor_critic.parameters(), lr=config.lr, betas=(0.9, 0.999)))

    # device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    # self.to(self.device)
    timesteps = range(10000)

    def run_single_timestep(engine, timestep):
        observation = engine.state.observation

        # select action from the policy
        observation = torch.Tensor(observation).to(device)
        action = choose_action(actor_critic, observation)

        engine.state.observation, reward, done, _, _ = env.step(action)

        if config.render:
            env.render()

        actor_critic.rewards.append(reward)
        engine.state.ep_reward += reward
        if done:
            engine.terminate_epoch()
            engine.state.timestep = timestep

    trainer = Engine(run_single_timestep)
    trainer.state.running_reward = 10

    @trainer.on(EPISODE_STARTED)
    def reset_environment_state():
        # reset environment and episode reward
        torch.manual_seed(config.seed + trainer.state.epoch)
        trainer.state.observation, _ = env.reset(seed=config.seed + trainer.state.epoch)
        trainer.state.ep_reward = 0

    @trainer.on(EPISODE_COMPLETED)
    def update_model():
        # update cumulative reward
        trainer.state.running_reward = 0.05 * trainer.state.ep_reward + (1 - 0.05) * trainer.state.running_reward
        # perform backprop
        learn(actor_critic, optimizer, config.gamma)

    @trainer.on(EPISODE_COMPLETED(every=config.log_every_episodes))
    def log_episode():
        i_episode = trainer.state.epoch
        print(
            f"Episode {i_episode}\tLast reward: {trainer.state.ep_reward:.2f}"
            f"\tAverage reward: {trainer.state.running_reward:.2f}"
        )

    @trainer.on(EPISODE_COMPLETED)
    def should_finish_training():
        # check if we have "solved" the cart pole problem
        running_reward = trainer.state.running_reward
        if running_reward > env.spec.reward_threshold:
            print(
                f"Solved! Running reward is now {running_reward} and "
                f"the last episode runs to {trainer.state.timestep} time steps!"
            )
            trainer.should_terminate = True

    trainer.run(timesteps, max_epochs=config.max_episodes)


def main():
    config = setup_config()
    env = gym.make("CarRacing-v2", continuous=False, render_mode="rgb_array" if config.render else None)
    with idist.Parallel(config.backend) as p:
        p.run(run, env=env, config=config)


if __name__ == "__main__":
    main()
