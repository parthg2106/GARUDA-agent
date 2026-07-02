"""Evaluation and benchmark scripts for GARUDA models."""

import torch
import numpy as np
from typing import Dict, Any, Tuple
from pathlib import Path
import json

from models.simulation_env import CombatSimulationEnv
from models.threat_assessment import ThreatAssessmentModel
from models.task_allocation import TaskAllocationNetwork
from models.formation_control import FormationControlNetwork
from models.mission_planning import DQNAgent
from models.workload_prediction import WorkloadPredictionLSTM
from app.config import settings
from app.utils.logger import logger


class ModelEvaluator:
    """Evaluates trained GARUDA models."""
    
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.results = {}
    
    def evaluate_threat_assessment(self, num_samples: int = 1000) -> Dict[str, float]:
        """Evaluate threat assessment model.
        
        Args:
            num_samples: Number of test samples
        
        Returns:
            Evaluation metrics
        """
        logger.info("Evaluating threat assessment model...")
        
        model = ThreatAssessmentModel(input_size=5)
        model.to(self.device)
        
        try:
            model.load("threat_assessment_best.pt")
        except:
            logger.warning("Could not load trained model")
        
        model.eval()
        
        # Generate test data
        X_test = torch.FloatTensor(np.random.rand(num_samples, 5)).to(self.device)
        
        with torch.no_grad():
            predictions = model(X_test)
        
        # Compute statistics
        metrics = {
            "mean_prediction": predictions.mean().item(),
            "std_prediction": predictions.std().item(),
            "min_prediction": predictions.min().item(),
            "max_prediction": predictions.max().item()
        }
        
        logger.info(f"Threat assessment metrics: {metrics}")
        return metrics
    
    def evaluate_mission_planning_in_env(self, num_episodes: int = 10) -> Dict[str, float]:
        """Evaluate mission planning in simulation environment.
        
        Args:
            num_episodes: Number of episodes
        
        Returns:
            Evaluation metrics
        """
        logger.info("Evaluating mission planning in simulation...")
        
        env = CombatSimulationEnv()
        agent = DQNAgent(state_size=10, num_actions=50)
        
        try:
            agent.load("mission_planning_final.pt")
        except:
            logger.warning("Could not load trained agent")
        
        episode_rewards = []
        mission_completions = []
        
        for ep in range(num_episodes):
            obs, _ = env.reset()
            total_reward = 0
            done = False
            
            while not done:
                action = agent.select_action(obs, training=False)
                obs, reward, terminated, truncated, info = env.step(
                    np.array([action % 2 - 0.5] * 8)  # Convert to continuous actions
                )
                total_reward += reward
                done = terminated or truncated
            
            episode_rewards.append(total_reward)
            mission_completions.append(info.get("mission_complete", False))
        
        metrics = {
            "avg_episode_reward": np.mean(episode_rewards),
            "std_episode_reward": np.std(episode_rewards),
            "mission_success_rate": np.mean(mission_completions),
            "max_episode_reward": np.max(episode_rewards)
        }
        
        logger.info(f"Mission planning metrics: {metrics}")
        return metrics
    
    def evaluate_formation_control(self, num_samples: int = 500) -> Dict[str, float]:
        """Evaluate formation control model.
        
        Args:
            num_samples: Number of test samples
        
        Returns:
            Evaluation metrics
        """
        logger.info("Evaluating formation control model...")
        
        model = FormationControlNetwork(input_size=12)
        model.to(self.device)
        
        try:
            model.load("formation_control_final.pt")
        except:
            logger.warning("Could not load trained model")
        
        model.eval()
        
        # Generate test data
        X_test = torch.FloatTensor(np.random.randn(num_samples, 12)).to(self.device)
        
        with torch.no_grad():
            velocities = model(X_test)
        
        # Compute statistics
        metrics = {
            "mean_velocity_x": velocities[:, 0].mean().item(),
            "mean_velocity_y": velocities[:, 1].mean().item(),
            "avg_velocity_magnitude": torch.norm(velocities, dim=1).mean().item(),
            "max_velocity_magnitude": torch.norm(velocities, dim=1).max().item()
        }
        
        logger.info(f"Formation control metrics: {metrics}")
        return metrics
    
    def run_complete_evaluation(self) -> Dict[str, Any]:
        """Run complete evaluation for all models.
        
        Returns:
            Complete evaluation results
        """
        logger.info("=" * 80)
        logger.info("Starting GARUDA Model Evaluation")
        logger.info("=" * 80)
        
        results = {}
        
        results["threat_assessment"] = self.evaluate_threat_assessment()
        results["formation_control"] = self.evaluate_formation_control()
        results["mission_planning"] = self.evaluate_mission_planning_in_env()
        
        logger.info("=" * 80)
        logger.info("Evaluation completed successfully!")
        logger.info("=" * 80)
        
        return results


if __name__ == "__main__":
    evaluator = ModelEvaluator()
    results = evaluator.run_complete_evaluation()
    print("\nEvaluation Results:")
    print(json.dumps(results, indent=2))
