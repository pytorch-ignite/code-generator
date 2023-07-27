import random
from collections import deque

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from utils import *

from shutil import copy

import ignite.distributed as idist

from ignite.engine import Engine, Events

from ignite.utils import manual_seed

from utils import *

try:
    import gymnasium as gym
except ImportError:
    raise ModuleNotFoundError("Please install opengym: pip install gymnasium[box2d]")

import numpy as np


class DQNetwork(nn.Module):
    def __init__(self, n_actions):
        super(DQNetwork, self).__init__()
        self.conv1 = nn.Conv2d(3, 8, kernel_size=4, stride=2)  # 3 * 96 * 96
        self.conv2 = nn.Conv2d(8, 16, kernel_size=3, stride=2)  # 32 * 47 * 47
        self.conv3 = nn.Conv2d(16, 32, kernel_size=3, stride=2)  # 64 * 22 * 22
        self.conv4 = nn.Conv2d(32, 64, kernel_size=3, stride=2)  # 128 * 10 * 10
        self.conv5 = nn.Conv2d(64, 128, kernel_size=3, stride=1)  # 256 * 6 * 6
        self.conv6 = nn.Conv2d(128, 256, kernel_size=3, stride=1)  # 256 * 6 * 6

        self.fc1 = nn.Linear(256, 100)
        self.fc2 = nn.Linear(100, 100)
        self.fc3 = nn.Linear(100, n_actions)
        self.float()

    def forward(self, x):
        x = torch.permute(x, (0, 3, 1, 2))

        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        x = F.relu(self.conv3(x))
        x = F.relu(self.conv4(x))
        x = F.relu(self.conv5(x))
        x = F.relu(self.conv6(x))

        x = x.reshape(-1, 256 * 1 * 1)

        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))

        return self.fc3(x)


EPISODE_STARTED = Events.EPOCH_STARTED
EPISODE_COMPLETED = Events.EPOCH_COMPLETED


def choose_action(engine, policy, observation):
    observation = observation.float().unsqueeze(0)

    policy.eval()
    with torch.no_grad():
        action = policy(observation)
    policy.train()

    sample = random.random()
    if sample > engine.epsilon:
        action = np.argmax(action.cpu().data.numpy())
        return action
    else:
        action = random.choice(np.arange(5))
        return action

    # return action


def learn(batch, batch_size, dqn, dqn_target, device, config, optimizer):
    criterion = torch.nn.MSELoss()

    states = np.zeros((batch_size, 96, 96, 3))

    next_states = np.zeros((batch_size, 96, 96, 3))

    actions, rewards, dones = [], [], []

    for i in range(batch_size):
        state_i, action_i, reward_i, next_state_i, done_i = batch[i]
        states[i] = state_i.cpu()
        next_states[i] = next_state_i
        actions.append(action_i)
        rewards.append(reward_i)
        dones.append(done_i)

    actions = np.vstack(actions).astype(int)
    actions = torch.from_numpy(actions).to(device)

    rewards = np.vstack(rewards).astype(float)
    rewards = torch.from_numpy(rewards).to(device)

    dones = np.vstack(dones).astype(int)
    dones = torch.from_numpy(dones).to(device)

    dqn.train()
    dqn_target.eval()

    predictions = dqn(torch.from_numpy(states).float().to(device)).gather(1, actions)

    with torch.no_grad():
        q_next = dqn_target(torch.from_numpy(next_states).float().to(device)).detach().max(1)[0].unsqueeze(1)

    targets = (rewards + (config.gamma * q_next * (1 - dones))).float()

    loss = criterion(predictions, targets).to(device)

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()


def main():
    config = setup_config()
    try:
        env = gym.make("CarRacing-v2", continuous=False, render_mode="rgb_array" if config.render else None)
    except ImportError:
        raise ModuleNotFoundError("Please install the 2D env: pip install gymnasium[box2d]")

    # make seed
    rank = idist.get_rank()
    manual_seed(config.seed + rank)

    config.output_dir = setup_output_dir(config, rank)
    if rank == 0:
        copy(config.config, f"{config.output_dir}/config-lock.yaml")

    buffer = deque(maxlen=10000)

    # Create wrapper for saving video
    if config.render:

        def trigger(episode):
            return episode % config.save_every_episodes == 0

        env = gym.wrappers.RecordVideo(env, config.recordings_path, trigger)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    dqn = DQNetwork(env.action_space.n).to(device)
    dqn_target = DQNetwork(env.action_space.n).to(device)

    optimizer = optim.Adam(dqn.parameters(), lr=config.lr)

    rewards = []

    def run_single_timestep(engine, timestep):
        observation = torch.Tensor(engine.state.observation).to(device)
        action = choose_action(engine, dqn, observation)

        next_observation, reward, done, _, _ = env.step(action)

        buffer.append((observation, action, reward, next_observation, done))

        engine.state.ep_reward += reward
        engine.state.next_observation = next_observation

        if done:
            engine.terminate_epoch()
            engine.state.timestep = timestep

    trainer = Engine(run_single_timestep)

    trainer.start_training = 3000
    trainer.epsilon = config.epsilon
    trainer.epsilon_min = config.epsilon_min
    trainer.epsilon_decay = config.epsilon_decay
    trainer.batch_size = config.batch_size

    trainer.state.cumulative_reward = []

    @trainer.on(Events.ITERATION_COMPLETED(every=500))
    def update_target_network():
        dqn_target.load_state_dict(dqn.state_dict())

    @trainer.on(Events.ITERATION_COMPLETED(every=4))
    def perform_learning():
        if len(buffer) >= trainer.start_training:
            if trainer.epsilon > trainer.epsilon_min:
                trainer.epsilon *= trainer.epsilon_decay
            minibatch = random.sample(buffer, min(len(buffer), trainer.batch_size))
            learn(minibatch, trainer.batch_size, dqn, dqn_target, device, config, optimizer)

    @trainer.on(Events.ITERATION_COMPLETED(every=1))
    def update_observations():
        trainer.state.observation = trainer.state.next_observation

    @trainer.on(EPISODE_STARTED)
    def reset_environment_state():
        trainer.state.observation, _ = env.reset()
        trainer.state.ep_reward = 0

    @trainer.on(EPISODE_COMPLETED)
    def update_rewards():
        rewards.append(trainer.state.ep_reward)

    @trainer.on(EPISODE_COMPLETED(every=config.log_every_episodes))
    def log_episode():
        print(f"Episode {trainer.state.epoch}; Reward for Episode: {trainer.state.ep_reward}, Current epsilon: {trainer.epsilon}")

    timesteps = range(config.steps_per_episode)
    trainer.run(timesteps, max_epochs=config.max_episodes)


if __name__ == "__main__":
    main()
