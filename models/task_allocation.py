"""Task Allocation Model using Multi-Agent Reinforcement Learning."""

import torch
import torch.nn as nn
import numpy as np
from typing import Tuple, Dict, Any, List
from pathlib import Path
from app.config import settings
from app.utils.logger import logger


class TaskAllocationNetwork(nn.Module):
    """Actor-Critic network for task allocation.
    
    Input: drone state + mission features
    Output: action logits + value estimate
    """
    
    def __init__(self, state_size: int = 20, num_actions: int = 10):
        super(TaskAllocationNetwork, self).__init__()
        self.state_size = state_size
        self.num_actions = num_actions
        
        # Shared feature extraction
        self.feature_net = nn.Sequential(
            nn.Linear(state_size, 256),
            nn.ReLU(),
            nn.Linear(256, 256),
            nn.ReLU()
        )
        
        # Actor head (action probabilities)
        self.actor = nn.Sequential(
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Linear(128, num_actions)
        )
        
        # Critic head (value estimate)
        self.critic = nn.Sequential(
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Linear(128, 1)
        )
    
    def forward(self, state: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        """Forward pass.
        
        Args:
            state: State tensor
        
        Returns:
            Action logits and value
        """
        features = self.feature_net(state)
        action_logits = self.actor(features)
        value = self.critic(features)
        return action_logits, value
    
    def save(self, filepath: str) -> None:
        """Save model.
        
        Args:
            filepath: Save path
        """
        path = Path(settings.MODEL_DIR) / filepath
        path.parent.mkdir(parents=True, exist_ok=True)
        torch.save(self.state_dict(), path)
        logger.info(f"Task allocation model saved to {path}")
    
    def load(self, filepath: str) -> None:
        """Load model.
        
        Args:
            filepath: Load path
        """
        path = Path(settings.MODEL_DIR) / filepath
        if path.exists():
            self.load_state_dict(torch.load(path))
            logger.info(f"Task allocation model loaded from {path}")


class TaskAllocationPPO:
    """PPO trainer for task allocation."""
    
    def __init__(
        self,
        network: TaskAllocationNetwork,
        learning_rate: float = 3e-4,
        gamma: float = 0.99,
        gae_lambda: float = 0.95,
        clip_ratio: float = 0.2
    ):
        self.network = network
        self.optimizer = torch.optim.Adam(network.parameters(), lr=learning_rate)
        self.gamma = gamma
        self.gae_lambda = gae_lambda
        self.clip_ratio = clip_ratio
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.network.to(self.device)
        self.training_history = []
    
    def compute_gae(
        self,
        rewards: List[float],
        values: List[float],
        next_value: float
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Compute Generalized Advantage Estimation.
        
        Args:
            rewards: Rewards list
            values: Value estimates
            next_value: Next state value
        
        Returns:
            Advantages and returns
        """
        advantages = []
        gae = 0
        
        for t in reversed(range(len(rewards))):
            if t == len(rewards) - 1:
                next_v = next_value
            else:
                next_v = values[t + 1]
            
            delta = rewards[t] + self.gamma * next_v - values[t]
            gae = delta + self.gamma * self.gae_lambda * gae
            advantages.insert(0, gae)
        
        advantages = np.array(advantages)
        returns = advantages + np.array(values)
        
        # Normalize advantages
        advantages = (advantages - advantages.mean()) / (advantages.std() + 1e-8)
        
        return advantages, returns
    
    def train_step(
        self,
        states: torch.Tensor,
        actions: torch.Tensor,
        old_log_probs: torch.Tensor,
        advantages: torch.Tensor,
        returns: torch.Tensor,
        num_epochs: int = 3
    ) -> float:
        """PPO training step.
        
        Args:
            states: State batch
            actions: Action batch
            old_log_probs: Old log probabilities
            advantages: Computed advantages
            returns: Computed returns
            num_epochs: Number of training epochs per batch
        
        Returns:
            Average loss
        """
        total_loss = 0
        
        for _ in range(num_epochs):
            action_logits, values = self.network(states)
            
            # Policy loss
            log_probs = torch.nn.functional.log_softmax(action_logits, dim=-1)
            log_probs = log_probs.gather(1, actions.unsqueeze(1)).squeeze(1)
            
            ratio = torch.exp(log_probs - old_log_probs)
            clipped_ratio = torch.clamp(ratio, 1 - self.clip_ratio, 1 + self.clip_ratio)
            
            policy_loss = -torch.min(
                ratio * advantages,
                clipped_ratio * advantages
            ).mean()
            
            # Value loss
            value_loss = nn.functional.mse_loss(values.squeeze(1), returns)
            
            # Total loss
            loss = policy_loss + 0.5 * value_loss
            
            self.optimizer.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(self.network.parameters(), 0.5)
            self.optimizer.step()
            
            total_loss += loss.item()
        
        avg_loss = total_loss / num_epochs
        self.training_history.append(avg_loss)
        return avg_loss
