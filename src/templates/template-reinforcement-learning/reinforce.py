from collections import deque

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

try:
    import gymnasium as gym
except ImportError:
    raise ModuleNotFoundError("Please install opengym: pip install gymnasium[box2d]")


eps = np.finfo(np.float32).eps.item()


class Policy(nn.Module):
    def __init__(self, state_dim, output_actions) -> None:
        super(Policy, self).__init__()

        self.conv = nn.Sequential(
            nn.Conv2d(state_dim, 32, kernel_size=3, stride=4),
            nn.ReLU(),
            nn.Conv2d(32, 64, kernel_size=1, stride=2),
            nn.ReLU(),
            nn.Conv2d(64, 64, kernel_size=1, stride=1),
            nn.ReLU(),
            nn.Flatten(),
        )

        conv_out_size = self._get_conv_out(state_dim)

        self.fc1 = nn.Linear(conv_out_size, 512)
        self.fc2 = nn.Linear(512, 128)
        self.fc3 = nn.Linear(128, output_actions)

        self.relu = nn.ReLU()

        self.saved_log_probs = []
        self.rewards = []

    def forward(self, x):
        x = self.conv(x)
        # x = self.dp(x)
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        x = self.relu(x)
        action_scores = self.fc3(x)
        return F.softmax(action_scores, dim=1)

    def _get_conv_out(self, shape):
        x = torch.zeros(1, *shape)
        x = self.conv(x)

        return int(np.prod(x.size()))


def choose_action(policy, observation):
    state = torch.from_numpy(observation).float().unsqueeze(0)
    probs = policy(state)
    m = Categorical(probs)
    action = m.sample()
    policy.saved_log_probs.append(m.log_prob(action))
    return action.item()


def learn(policy, optimizer, gamma):
    R = 0
    policy_loss = []
    returns = deque()
    for r in policy.rewards[::-1]:
        R = r + gamma * R
        returns.appendleft(R)
    returns = torch.tensor(returns)
    returns = (returns - returns.mean()) / (returns.std() + eps)
    for log_prob, R in zip(policy.saved_log_probs, returns):
        policy_loss.append(-log_prob * R)
    optimizer.zero_grad()
    policy_loss = torch.cat(policy_loss).sum()
    policy_loss.backward()
    optimizer.step()
    del policy.rewards[:]
    del policy.saved_log_probs[:]


EPISODE_STARTED = Events.EPOCH_STARTED
EPISODE_COMPLETED = Events.EPOCH_COMPLETED


def run(local_rank: int, env: Any, config: Any):
    # make seed
    rank = idist.get_rank()
    manual_seed(config.seed + rank)

    # create output folder and copy config file to output dir
    config.output_dir = setup_output_dir(config, rank)
    if rank == 0:
        copy(config.config, f"{config.output_dir}/config-lock.yaml")

    # create wrapper for saving video
    if config.render:

        def trigger(episode):
            return episode % config.save_every_episode == 0

        env = gym.wrappers.RecordVideo(env, config.recordings_path, trigger)

    # device, policy, optimizer
    device = idist.device()
    policy = Policy(env.observation_space.shape[0], env.action_space.n).to(device)

    optimizer = idist.auto_optim(optim.Adam(actor_critic.parameters(), lr=config.lr, betas=(0.9, 0.999)))

    # device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    # self.to(self.device)
    timesteps = range(10000)

    def run_single_timestep(engine, timestep):
        observation = engine.state.observation

        # select action from the policy
        observation = torch.Tensor(observation).to(device)
        action = choose_action(policy, observation)

        engine.state.observation, reward, done, _, _ = env.step(action)

        if config.render:
            env.render()

        policy.rewards.append(reward)
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
        learn(policy, optimizer, config.gamma)

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
