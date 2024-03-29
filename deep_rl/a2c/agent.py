from typing import List

import numpy as np
import torch
from torch import nn
from torch.distributions import Categorical

class ActorCriticAgent:
    """Actor-Critic based agent that returns an action based on the networks policy."""

    def __init__(self, net):
        self.net = net

    def __call__(self, states: torch.Tensor, device: str) -> List[int]:
        """Takes in the current state and returns the action based on the agents policy.
        Args:
            states: current state of the environment
            device: the device used for the current batch
        Returns:
            action defined by policy
        """
        logprobs, _ = self.net(torch.tensor([states], device=device))
        probabilities = logprobs.exp().squeeze(dim=-1)
        prob_np = probabilities.data.cpu().numpy()

        # take the numpy values and randomly select action based on prob distribution
        # Note that this is much faster than numpy.random.choice
        cdf = np.cumsum(prob_np, axis=1)
        cdf[:, -1] = 1.  # Ensure cumsum adds to 1
        select = np.random.random(cdf.shape[0])
        actions = [
            np.searchsorted(cdf[row, :], select[row])
            for row in range(cdf.shape[0])
        ]

        return actions

class ActorCategorical(nn.Module):
    """Policy network, for discrete action spaces, which returns a distribution and an action given an
    observation."""

    def __init__(self, actor_net: nn.Module) -> None:
        """
        Args:
            actor_net: neural network that predicts action probabilities given the env state
        """
        super().__init__()

        self.actor_net = actor_net

    def forward(self, states):
        logits = self.actor_net(states)
        pi = Categorical(logits=logits)
        actions = pi.sample()

        return pi, actions


class GreedyActorCriticAgent:
    def __init__(self, net):
        self.net = net

    def __call__(self, states: torch.Tensor, device: str) -> List[int]:
        """Takes in the current state and returns the action based on the agents policy.
        Args:
            states: current state of the environment
            device: the device used for the current batch
        Returns:
            action defined by policy
        """
        logprobs, _ = self.net(torch.tensor([states], device=device))
        probabilities = logprobs.exp().squeeze(dim=-1)
        prob_np = probabilities.data.cpu().numpy()

        actions = np.argmax(prob_np, axis=1)

        return list(actions)
