from typing import Tuple

import numpy as np
import torch
from torch import Tensor, nn
import gym

from deep_q.experience import SequenceReplay, Experience


class Agent:
    """Base Agent class handeling the interaction with the environment."""

    def __init__(self, env: gym.Env, replay_buffer: SequenceReplay) -> None:
        """
        Args:
            env: training environment
            replay_buffer: replay buffer storing experiences
        """
        self.env = env
        self.replay_buffer = replay_buffer
        self.reset()
        self.state = self.env.reset()

    def reset(self) -> None:
        """Resents the environment and updates the state."""
        self.state = self.env.reset()

    def get_action(self, net: nn.Module, epsilon: float, device: str) -> int:
        """Using the given network, decide what action to carry out using an epsilon-greedy policy.

        Args:
            net: DQN network
            epsilon: value to determine likelihood of taking a random action
            device: current device

        Returns:
            action
        """
        if np.random.random() < epsilon:
            action = self.env.action_space.sample()
        else:
            state = torch.tensor([self.state]).to(device)
            q_values = net(state)
            _, action = torch.max(q_values, dim=1)
            action = int(action.item())

        return action

    def play_game(
            self,
            net: nn.Module,
            epsilon: float = 0.0,
            device: str = "cpu",
    ) -> Tuple[float, bool]:

        done = False
        cur_seq = list()
        reward = 0
        while not done:
            reward, done, exp = self.play_step(net, epsilon, device)
            cur_seq.append(exp)

        winning_steps = self.env.max_turns - self.state[0]
        if reward > 0:
            self.replay_buffer.append_winner(cur_seq)
        else:
            self.replay_buffer.append_loser(cur_seq)
        self.reset()

        return reward, winning_steps

    @torch.no_grad()
    def play_step(
            self,
            net: nn.Module,
            epsilon: float = 0.0,
            device: str = "cpu",
    ) -> Tuple[float, bool, Experience]:
        """Carries out a single interaction step between the agent and the environment.

        Args:
            net: DQN network
            epsilon: value to determine likelihood of taking a random action
            device: current device

        Returns:
            reward, done
        """

        action = self.get_action(net, epsilon, device)

        # do step in the environment
        new_state, reward, done, _ = self.env.step(action)

        exp = Experience(self.state, action, reward, done, new_state)

        self.state = new_state
        return reward, done, exp
