"""Training scripts for GARUDA models."""

import torch
from torch.utils.data import TensorDataset, DataLoader
import numpy as np
from typing import Dict, Any
from pathlib import Path
import json

from models.threat_assessment import ThreatAssessmentModel, ThreatAssessmentTrainer
from models.task_allocation import TaskAllocationNetwork, TaskAllocationPPO
from models.formation_control import FormationControlNetwork, FormationControlTrainer
from models.mission_planning import DQNAgent
from models.workload_prediction import WorkloadPredictionLSTM, WorkloadTrainer
from training.data_generation import DataGenerator
from app.config import settings
from app.utils.logger import logger
from app.utils.metrics import MetricsCollector


class TrainingPipeline:
    """Complete training pipeline for GARUDA models."""
    
    def __init__(self):
        self.data_gen = DataGenerator()
        self.metrics = MetricsCollector()
    
    def train_threat_assessment(self, epochs: int = 100) -> Dict[str, Any]:
        """Train threat assessment model.
        
        Args:
            epochs: Number of training epochs
        
        Returns:
            Training results
        """
        logger.info("Starting threat assessment model training...")
        
        # Generate data
        X, y = self.data_gen.generate_threat_assessment_data(num_samples=5000)
        self.data_gen.save_dataset("threat_assessment", X, y)
        
        # Split data
        split_idx = int(0.8 * len(X))
        X_train, X_val = X[:split_idx], X[split_idx:]
        y_train, y_val = y[:split_idx], y[split_idx:]
        
        # Create data loaders
        train_dataset = TensorDataset(
            torch.FloatTensor(X_train),
            torch.FloatTensor(y_train)
        )
        val_dataset = TensorDataset(
            torch.FloatTensor(X_val),
            torch.FloatTensor(y_val)
        )
        
        train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
        val_loader = DataLoader(val_dataset, batch_size=64, shuffle=False)
        
        # Initialize model and trainer
        model = ThreatAssessmentModel(input_size=5)
        trainer = ThreatAssessmentTrainer(model)
        
        # Train
        history = trainer.train(train_loader, val_loader, epochs=epochs)
        
        # Save model
        model.save("threat_assessment_final.pt")
        
        logger.info("Threat assessment training completed")
        self.metrics.record_metric("threat_assessment_final_loss", history["val_loss"][-1])
        
        return history
    
    def train_task_allocation(self, episodes: int = 1000) -> Dict[str, Any]:
        """Train task allocation model using PPO.
        
        Args:
            episodes: Number of episodes
        
        Returns:
            Training results
        """
        logger.info("Starting task allocation model training...")
        
        # Generate data
        episode_data = self.data_gen.generate_task_allocation_data(num_episodes=episodes)
        self.data_gen.save_episodes("task_allocation", episode_data)
        
        # Initialize network and trainer
        network = TaskAllocationNetwork(state_size=20, num_actions=10)
        trainer = TaskAllocationPPO(network)
        
        # Training loop
        for ep_idx, episode in enumerate(episode_data[:100]):  # Train on 100 episodes
            states = np.array(episode["states"], dtype=np.float32)
            actions = np.array(episode["actions"])
            rewards = np.array(episode["rewards"])
            
            # Compute advantages
            values = []
            with torch.no_grad():
                for state in states:
                    _, value = network(torch.FloatTensor(state).unsqueeze(0))
                    values.append(value.item())
            
            advantages, returns = trainer.compute_gae(rewards.tolist(), values, 0)
            
            # Training step
            loss = trainer.train_step(
                torch.FloatTensor(states),
                torch.LongTensor(actions),
                torch.FloatTensor(np.zeros(len(actions))),  # Placeholder log probs
                torch.FloatTensor(advantages),
                torch.FloatTensor(returns)
            )
            
            if (ep_idx + 1) % 20 == 0:
                logger.info(f"Task allocation episode {ep_idx + 1}/{100}, Loss: {loss:.4f}")
        
        # Save model
        network.save("task_allocation_final.pt")
        
        logger.info("Task allocation training completed")
        
        return {"avg_loss": np.mean(trainer.training_history)}
    
    def train_formation_control(self, epochs: int = 50) -> Dict[str, Any]:
        """Train formation control model.
        
        Args:
            epochs: Number of epochs
        
        Returns:
            Training results
        """
        logger.info("Starting formation control model training...")
        
        # Generate data
        X, y = self.data_gen.generate_formation_control_data(num_samples=5000)
        self.data_gen.save_dataset("formation_control", X, y)
        
        # Create data loader
        dataset = TensorDataset(
            torch.FloatTensor(X),
            torch.FloatTensor(y)
        )
        train_loader = DataLoader(dataset, batch_size=64, shuffle=True)
        
        # Initialize model and trainer
        model = FormationControlNetwork(input_size=12)
        trainer = FormationControlTrainer(model)
        
        # Train
        for epoch in range(epochs):
            avg_loss = trainer.train_epoch(train_loader)
            if (epoch + 1) % 10 == 0:
                logger.info(f"Formation control epoch {epoch + 1}/{epochs}, Loss: {avg_loss:.4f}")
        
        # Save model
        model.save("formation_control_final.pt")
        
        logger.info("Formation control training completed")
        
        return {"final_loss": trainer.training_history[-1]}
    
    def train_mission_planning(self, episodes: int = 500) -> Dict[str, Any]:
        """Train mission planning model using DQN.
        
        Args:
            episodes: Number of episodes
        
        Returns:
            Training results
        """
        logger.info("Starting mission planning model training...")
        
        # Generate data
        episode_data = self.data_gen.generate_mission_planning_data(num_episodes=episodes)
        self.data_gen.save_episodes("mission_planning", episode_data)
        
        # Initialize agent
        agent = DQNAgent(state_size=10, num_actions=50)
        
        # Training loop
        for ep_idx, episode in enumerate(episode_data[:100]):
            states = np.array(episode["states"], dtype=np.float32)
            actions = np.array(episode["actions"])
            rewards = np.array(episode["rewards"], dtype=np.float32)
            
            # Add experiences to replay buffer
            for i in range(len(states) - 1):
                agent.replay_buffer.add(
                    states[i],
                    actions[i],
                    rewards[i],
                    states[i + 1],
                    i == len(states) - 2
                )
            
            # Train on batch
            for _ in range(10):
                loss = agent.train_step(batch_size=32)
            
            # Update target network
            if (ep_idx + 1) % 10 == 0:
                agent.update_target_network()
                logger.info(f"Mission planning episode {ep_idx + 1}/{100}")
        
        # Save model
        agent.save("mission_planning_final.pt")
        
        logger.info("Mission planning training completed")
        
        return {"avg_loss": np.mean(agent.training_history[-100:])}
    
    def train_workload_prediction(self, epochs: int = 100) -> Dict[str, Any]:
        """Train workload prediction model.
        
        Args:
            epochs: Number of epochs
        
        Returns:
            Training results
        """
        logger.info("Starting workload prediction model training...")
        
        # Generate data
        X, y = self.data_gen.generate_workload_prediction_data(num_samples=3000)
        self.data_gen.save_dataset("workload_prediction", X, y)
        
        # Split data
        split_idx = int(0.8 * len(X))
        X_train, X_val = X[:split_idx], X[split_idx:]
        y_train, y_val = y[:split_idx], y[split_idx:]
        
        # Create data loaders
        train_dataset = TensorDataset(
            torch.FloatTensor(X_train),
            torch.FloatTensor(y_train)
        )
        val_dataset = TensorDataset(
            torch.FloatTensor(X_val),
            torch.FloatTensor(y_val)
        )
        
        train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
        val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False)
        
        # Initialize model and trainer
        model = WorkloadPredictionLSTM(input_size=10, hidden_size=128)
        trainer = WorkloadTrainer(model)
        
        # Train
        for epoch in range(epochs):
            train_loss = trainer.train_epoch(train_loader)
            val_loss = trainer.validate(val_loader)
            
            if (epoch + 1) % 20 == 0:
                logger.info(
                    f"Workload prediction epoch {epoch + 1}/{epochs}, "
                    f"Train Loss: {train_loss:.4f}, Val Loss: {val_loss:.4f}"
                )
        
        # Save model
        model.save("workload_prediction_final.pt")
        
        logger.info("Workload prediction training completed")
        
        return {"final_val_loss": val_loss}
    
    def run_complete_training(self) -> Dict[str, Any]:
        """Run complete training pipeline for all models.
        
        Returns:
            Complete training results
        """
        logger.info("=" * 80)
        logger.info("Starting GARUDA Complete Training Pipeline")
        logger.info("=" * 80)
        
        results = {}
        
        # Train all models
        results["threat_assessment"] = self.train_threat_assessment(epochs=50)
        results["task_allocation"] = self.train_task_allocation(episodes=500)
        results["formation_control"] = self.train_formation_control(epochs=30)
        results["mission_planning"] = self.train_mission_planning(episodes=500)
        results["workload_prediction"] = self.train_workload_prediction(epochs=50)
        
        logger.info("=" * 80)
        logger.info("Training pipeline completed successfully!")
        logger.info("=" * 80)
        
        # Export metrics
        metrics_summary = self.metrics.export_metrics("training_metrics.json")
        results["metrics"] = metrics_summary
        
        return results


if __name__ == "__main__":
    pipeline = TrainingPipeline()
    results = pipeline.run_complete_training()
    print("\nTraining Results:")
    print(json.dumps({k: v for k, v in results.items() if k != "metrics"}, indent=2))
