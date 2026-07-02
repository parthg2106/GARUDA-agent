"""Formation Control Model using swarm intelligence principles."""

import torch
import torch.nn as nn
import numpy as np
from typing import Tuple, Dict, Any, List
from pathlib import Path
from app.config import settings
from app.utils.logger import logger


class FormationControlNetwork(nn.Module):
    """Neural network for formation control.
    
    Input: relative positions and velocities of neighbors
    Output: velocity commands for drone
    """
    
    def __init__(self, input_size: int = 12, hidden_size: int = 128):
        super(FormationControlNetwork, self).__init__()
        self.input_size = input_size
        
        self.net = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, 2)  # Output: [vx, vy]
        )
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Forward pass.
        
        Args:
            x: Input tensor
        
        Returns:
            Velocity commands
        """
        return self.net(x)
    
    def save(self, filepath: str) -> None:
        """Save model.
        
        Args:
            filepath: Save path
        """
        path = Path(settings.MODEL_DIR) / filepath
        path.parent.mkdir(parents=True, exist_ok=True)
        torch.save(self.state_dict(), path)
        logger.info(f"Formation control model saved to {path}")
    
    def load(self, filepath: str) -> None:
        """Load model.
        
        Args:
            filepath: Load path
        """
        path = Path(settings.MODEL_DIR) / filepath
        if path.exists():
            self.load_state_dict(torch.load(path))
            logger.info(f"Formation control model loaded from {path}")


class FormationControlTrainer:
    """Trainer for formation control using swarm algorithms."""
    
    def __init__(self, model: FormationControlNetwork, learning_rate: float = 0.001):
        self.model = model
        self.optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
        self.training_history = []
    
    def compute_formation_loss(
        self,
        current_positions: torch.Tensor,
        target_formation: torch.Tensor,
        velocity_commands: torch.Tensor
    ) -> torch.Tensor:
        """Compute formation control loss.
        
        Args:
            current_positions: Current drone positions
            target_formation: Target formation positions
            velocity_commands: Predicted velocity commands
        
        Returns:
            Loss tensor
        """
        # Distance to target formation
        position_loss = torch.norm(current_positions - target_formation, dim=1).mean()
        
        # Smoothness of velocities (minimize jerky movements)
        velocity_smoothness = torch.norm(velocity_commands, dim=1).mean()
        
        # Total loss
        loss = position_loss + 0.1 * velocity_smoothness
        return loss
    
    def train_epoch(self, train_loader) -> float:
        """Train one epoch.
        
        Args:
            train_loader: Training data loader
        
        Returns:
            Average loss
        """
        self.model.train()
        total_loss = 0.0
        
        for batch in train_loader:
            X, target_formation = batch
            X = X.to(self.device)
            target_formation = target_formation.to(self.device)
            
            self.optimizer.zero_grad()
            velocity_commands = self.model(X)
            loss = self.compute_formation_loss(X, target_formation, velocity_commands)
            loss.backward()
            self.optimizer.step()
            
            total_loss += loss.item()
        
        avg_loss = total_loss / len(train_loader)
        self.training_history.append(avg_loss)
        return avg_loss
