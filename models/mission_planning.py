"""Mission Planning Model using DQN (Deep Q-Network)."""

import torch
import torch.nn as nn
import numpy as np
from collections import deque
from typing import Tuple, Dict, Any, List, Optional
from pathlib import Path
from app.config import settings
from app.utils.logger import logger


class QNetwork(nn.Module):
    """Deep Q-Network for mission planning.
    
    Input: mission state (current location, target, threats, fuel)
    Output: Q-values for each possible action (waypoint)
    """
    
    def __init__(self, state_size: int = 10, num_actions: int = 50):
        super(QNetwork, self).__init__()
        self.state_size = state_size
        self.num_actions = num_actions
        
        self.net = nn.Sequential(
            nn.Linear(state_size, 256),
            nn.ReLU(),
            nn.Linear(256, 256),
            nn.ReLU(),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Linear(128, num_actions)
        )
    
    def forward(self, state: torch.Tensor) -> torch.Tensor:
        """Forward pass.
        
        Args:
            state: State tensor
        
        Returns:
            Q-values for each action
        """
        return self.net(state)
    
    def save(self, filepath: str) -> None:
        """Save model.
        
        Args:
            filepath: Save path
        """
        path = Path(settings.MODEL_DIR) / filepath
        path.parent.mkdir(parents=True, exist_ok=True)
        torch.save(self.state_dict(), path)
        logger.info(f"Q-Network model saved to {path}")
    
    def load(self, filepath: str) -> None:
        """Load model.
        
        Args:
            filepath: Load path
        """
        path = Path(settings.MODEL_DIR) / filepath
        if path.exists():
            self.load_state_dict(torch.load(path))
            logger.info(f"Q-Network model loaded from {path}")


class ReplayBuffer:
    """Experience replay buffer for DQN training."""
    
    def __init__(self, max_size: int = 10000):
        self.buffer = deque(maxlen=max_size)
    
    def add(
        self,
        state: np.ndarray,
        action: int,
        reward: float,
        next_state: np.ndarray,
        done: bool
    ) -> None:
        """Add experience to buffer.
        
        Args:
            state: State
            action: Action
            reward: Reward
            next_state: Next state
            done: Episode done flag
        """
        self.buffer.append((state, action, reward, next_state, done))
    
    def sample(self, batch_size: int) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
        """Sample batch from buffer.
        
        Args:
            batch_size: Batch size
        
        Returns:
            Batch of experiences
        """
        indices = np.random.choice(len(self.buffer), batch_size, replace=False)
        states, actions, rewards, next_states, dones = zip(*[self.buffer[i] for i in indices])
        
        return (
            torch.FloatTensor(np.array(states)),
            torch.LongTensor(actions),
            torch.FloatTensor(rewards),
            torch.FloatTensor(np.array(next_states)),
            torch.FloatTensor(dones)
        )
    
    def __len__(self) -> int:
        return len(self.buffer)


class DQNAgent:
    """DQN Agent for mission planning."""
    
    def __init__(
        self,
        state_size: int = 10,
        num_actions: int = 50,
        learning_rate: float = 0.0001,
        gamma: float = 0.99,
        epsilon: float = 1.0,
        epsilon_decay: float = 0.995,
        epsilon_min: float = 0.01
    ):
        self.state_size = state_size
        self.num_actions = num_actions
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min
        
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        # Networks
        self.q_network = QNetwork(state_size, num_actions).to(self.device)
        self.target_network = QNetwork(state_size, num_actions).to(self.device)
        self.target_network.load_state_dict(self.q_network.state_dict())
        
        self.optimizer = torch.optim.Adam(self.q_network.parameters(), lr=learning_rate)
        self.loss_fn = nn.MSELoss()
        
        # Replay buffer
        self.replay_buffer = ReplayBuffer()
        self.training_history = []
    
    def select_action(self, state: np.ndarray, training: bool = True) -> int:
        """Select action using epsilon-greedy policy.
        
        Args:
            state: Current state
            training: Training mode flag
        
        Returns:
            Selected action
        """
        if training and np.random.rand() < self.epsilon:
            return np.random.randint(self.num_actions)
        
        with torch.no_grad():
            state_tensor = torch.FloatTensor(state).unsqueeze(0).to(self.device)
            q_values = self.q_network(state_tensor)
            return q_values.argmax(1).item()
    
    def train_step(self, batch_size: int = 32) -> float:
        """DQN training step.
        
        Args:
            batch_size: Batch size
        
        Returns:
            Loss
        """
        if len(self.replay_buffer) < batch_size:
            return 0.0
        
        states, actions, rewards, next_states, dones = self.replay_buffer.sample(batch_size)
        
        states = states.to(self.device)
        actions = actions.to(self.device)
        rewards = rewards.to(self.device)
        next_states = next_states.to(self.device)
        dones = dones.to(self.device)
        
        # Compute Q-targets
        with torch.no_grad():
            next_q_values = self.target_network(next_states).max(1)[0]
            q_targets = rewards + self.gamma * next_q_values * (1 - dones)
        
        # Compute Q-predictions
        q_predictions = self.q_network(states).gather(1, actions.unsqueeze(1)).squeeze(1)
        
        # Compute loss
        loss = self.loss_fn(q_predictions, q_targets)
        
        # Backprop
        self.optimizer.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(self.q_network.parameters(), 1.0)
        self.optimizer.step()
        
        # Update epsilon
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)
        
        self.training_history.append(loss.item())
        return loss.item()
    
    def update_target_network(self) -> None:
        """Update target network."""
        self.target_network.load_state_dict(self.q_network.state_dict())
    
    def save(self, filepath: str) -> None:
        """Save model.
        
        Args:
            filepath: Save path
        """
        path = Path(settings.MODEL_DIR) / filepath
        path.parent.mkdir(parents=True, exist_ok=True)
        torch.save(self.q_network.state_dict(), path)
        logger.info(f"DQN Agent model saved to {path}")
    
    def load(self, filepath: str) -> None:
        """Load model.
        
        Args:
            filepath: Load path
        """
        self.q_network.load(filepath)
        self.target_network.load_state_dict(self.q_network.state_dict())
