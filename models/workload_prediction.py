"""Pilot Workload Prediction Model."""

import torch
import torch.nn as nn
import numpy as np
from typing import Tuple, Dict, Any
from pathlib import Path
from app.config import settings
from app.utils.logger import logger


class WorkloadPredictionLSTM(nn.Module):
    """LSTM network for predicting pilot workload.
    
    Input: sequence of workload indicators
    Output: workload level prediction
    """
    
    def __init__(
        self,
        input_size: int = 10,
        hidden_size: int = 128,
        num_layers: int = 2,
        dropout: float = 0.3
    ):
        super(WorkloadPredictionLSTM, self).__init__()
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        
        self.lstm = nn.LSTM(
            input_size=input_size,
            hidden_size=hidden_size,
            num_layers=num_layers,
            dropout=dropout if num_layers > 1 else 0,
            batch_first=True
        )
        
        self.fc = nn.Sequential(
            nn.Linear(hidden_size, 64),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(64, 1),
            nn.Sigmoid()  # Output workload 0-1
        )
    
    def forward(
        self,
        x: torch.Tensor,
        hidden: Tuple[torch.Tensor, torch.Tensor] = None
    ) -> Tuple[torch.Tensor, Tuple[torch.Tensor, torch.Tensor]]:
        """Forward pass.
        
        Args:
            x: Input sequences [batch, seq_len, input_size]
            hidden: Initial hidden states
        
        Returns:
            Workload predictions and hidden states
        """
        lstm_out, hidden = self.lstm(x, hidden)
        # Use last output
        last_output = lstm_out[:, -1, :]
        workload = self.fc(last_output)
        return workload, hidden
    
    def save(self, filepath: str) -> None:
        """Save model.
        
        Args:
            filepath: Save path
        """
        path = Path(settings.MODEL_DIR) / filepath
        path.parent.mkdir(parents=True, exist_ok=True)
        torch.save(self.state_dict(), path)
        logger.info(f"Workload prediction model saved to {path}")
    
    def load(self, filepath: str) -> None:
        """Load model.
        
        Args:
            filepath: Load path
        """
        path = Path(settings.MODEL_DIR) / filepath
        if path.exists():
            self.load_state_dict(torch.load(path))
            logger.info(f"Workload prediction model loaded from {path}")


class WorkloadTrainer:
    """Trainer for workload prediction model."""
    
    def __init__(
        self,
        model: WorkloadPredictionLSTM,
        learning_rate: float = 0.001,
        weight_decay: float = 1e-5
    ):
        self.model = model
        self.optimizer = torch.optim.Adam(
            model.parameters(),
            lr=learning_rate,
            weight_decay=weight_decay
        )
        self.loss_fn = nn.BCELoss()
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
        self.training_history = []
    
    def train_epoch(self, train_loader) -> float:
        """Train one epoch.
        
        Args:
            train_loader: Training data loader
        
        Returns:
            Average loss
        """
        self.model.train()
        total_loss = 0.0
        
        for X, y in train_loader:
            X = X.to(self.device)
            y = y.to(self.device).unsqueeze(1)
            
            self.optimizer.zero_grad()
            predictions, _ = self.model(X)
            loss = self.loss_fn(predictions, y)
            loss.backward()
            self.optimizer.step()
            
            total_loss += loss.item()
        
        avg_loss = total_loss / len(train_loader)
        self.training_history.append(avg_loss)
        return avg_loss
    
    def validate(self, val_loader) -> float:
        """Validate model.
        
        Args:
            val_loader: Validation data loader
        
        Returns:
            Validation loss
        """
        self.model.eval()
        total_loss = 0.0
        
        with torch.no_grad():
            for X, y in val_loader:
                X = X.to(self.device)
                y = y.to(self.device).unsqueeze(1)
                
                predictions, _ = self.model(X)
                loss = self.loss_fn(predictions, y)
                total_loss += loss.item()
        
        return total_loss / len(val_loader)
