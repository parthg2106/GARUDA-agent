"""Threat Assessment Model using supervised learning."""

import torch
import torch.nn as nn
import numpy as np
from typing import Tuple, Dict, Any
from pathlib import Path
from app.config import settings
from app.utils.logger import logger


class ThreatAssessmentModel(nn.Module):
    """Neural network for threat assessment.
    
    Input: [distance, drone_count, altitude, speed, radar_signature]
    Output: threat_level (0-1)
    """
    
    def __init__(self, input_size: int = 5, hidden_size: int = 128):
        super(ThreatAssessmentModel, self).__init__()
        self.input_size = input_size
        self.hidden_size = hidden_size
        
        self.net = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(hidden_size, 64),
            nn.ReLU(),
            nn.Linear(64, 1),
            nn.Sigmoid()  # Output threat level 0-1
        )
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Forward pass.
        
        Args:
            x: Input tensor
        
        Returns:
            Threat level prediction
        """
        return self.net(x)
    
    def save(self, filepath: str) -> None:
        """Save model to file.
        
        Args:
            filepath: Save path
        """
        path = Path(settings.MODEL_DIR) / filepath
        path.parent.mkdir(parents=True, exist_ok=True)
        torch.save(self.state_dict(), path)
        logger.info(f"Threat assessment model saved to {path}")
    
    def load(self, filepath: str) -> None:
        """Load model from file.
        
        Args:
            filepath: Load path
        """
        path = Path(settings.MODEL_DIR) / filepath
        if path.exists():
            self.load_state_dict(torch.load(path))
            logger.info(f"Threat assessment model loaded from {path}")
        else:
            logger.warning(f"Model file not found: {path}")


class ThreatAssessmentTrainer:
    """Trainer for threat assessment model."""
    
    def __init__(self, model: ThreatAssessmentModel, learning_rate: float = 0.001):
        self.model = model
        self.optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
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
            predictions = self.model(X)
            loss = self.loss_fn(predictions, y)
            loss.backward()
            self.optimizer.step()
            
            total_loss += loss.item()
        
        avg_loss = total_loss / len(train_loader)
        self.training_history.append(avg_loss)
        return avg_loss
    
    def validate(self, val_loader) -> Tuple[float, float]:
        """Validate model.
        
        Args:
            val_loader: Validation data loader
        
        Returns:
            Validation loss and accuracy
        """
        self.model.eval()
        total_loss = 0.0
        correct = 0
        total = 0
        
        with torch.no_grad():
            for X, y in val_loader:
                X = X.to(self.device)
                y = y.to(self.device).unsqueeze(1)
                
                predictions = self.model(X)
                loss = self.loss_fn(predictions, y)
                total_loss += loss.item()
                
                # Binary classification
                pred_labels = (predictions > 0.5).float()
                correct += (pred_labels == y).sum().item()
                total += y.size(0)
        
        avg_loss = total_loss / len(val_loader)
        accuracy = correct / total if total > 0 else 0
        
        return avg_loss, accuracy
    
    def train(
        self,
        train_loader,
        val_loader,
        epochs: int = 100,
        patience: int = 10
    ) -> Dict[str, Any]:
        """Train model with early stopping.
        
        Args:
            train_loader: Training data loader
            val_loader: Validation data loader
            epochs: Number of epochs
            patience: Early stopping patience
        
        Returns:
            Training history
        """
        best_val_loss = float('inf')
        patience_counter = 0
        history = {"train_loss": [], "val_loss": [], "val_accuracy": []}
        
        for epoch in range(epochs):
            train_loss = self.train_epoch(train_loader)
            val_loss, val_acc = self.validate(val_loader)
            
            history["train_loss"].append(train_loss)
            history["val_loss"].append(val_loss)
            history["val_accuracy"].append(val_acc)
            
            if (epoch + 1) % 10 == 0:
                logger.info(
                    f"Epoch {epoch+1}/{epochs} - "
                    f"Train Loss: {train_loss:.4f}, "
                    f"Val Loss: {val_loss:.4f}, "
                    f"Val Acc: {val_acc:.4f}"
                )
            
            # Early stopping
            if val_loss < best_val_loss:
                best_val_loss = val_loss
                patience_counter = 0
                self.model.save("threat_assessment_best.pt")
            else:
                patience_counter += 1
                if patience_counter >= patience:
                    logger.info(f"Early stopping at epoch {epoch+1}")
                    break
        
        return history
