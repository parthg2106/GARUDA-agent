"""Data generation for training datasets."""

import numpy as np
import torch
from typing import Tuple, List, Dict, Any
from pathlib import Path
import json
from app.config import settings


class DataGenerator:
    """Generates synthetic training data for GARUDA models."""
    
    def __init__(self, seed: int = 42):
        np.random.seed(seed)
        self.data_dir = Path(settings.TRAINING_OUTPUT_DIR) / "datasets"
        self.data_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_threat_assessment_data(
        self,
        num_samples: int = 5000
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Generate threat assessment training data.
        
        Args:
            num_samples: Number of samples to generate
        
        Returns:
            Features and labels
        """
        # Features: [distance, drone_count, altitude, speed, radar_signature]
        X = np.random.rand(num_samples, 5)
        X[:, 0] *= 100  # distance (0-100)
        X[:, 1] *= 10   # drone_count (0-10)
        X[:, 2] *= 10000  # altitude (0-10000)
        X[:, 3] *= 100  # speed (0-100)
        X[:, 4] *= 1    # radar_signature (0-1)
        
        # Generate labels based on features
        y = np.zeros(num_samples)
        # High threat: high signature, low distance, high speed
        high_threat = (X[:, 4] > 0.7) & (X[:, 0] < 30) & (X[:, 3] > 50)
        y[high_threat] = 1
        
        # Noise
        noise_idx = np.random.choice(num_samples, int(0.1 * num_samples), replace=False)
        y[noise_idx] = 1 - y[noise_idx]
        
        return X.astype(np.float32), y.astype(np.float32)
    
    def generate_task_allocation_data(
        self,
        num_episodes: int = 1000
    ) -> List[Dict[str, Any]]:
        """Generate task allocation training data.
        
        Args:
            num_episodes: Number of episodes
        
        Returns:
            List of episodes
        """
        episodes = []
        
        for _ in range(num_episodes):
            episode = {
                "states": [],
                "actions": [],
                "rewards": [],
                "dones": []
            }
            
            num_steps = np.random.randint(10, 100)
            for _ in range(num_steps):
                # Random drone state: [position, velocity, battery, status]
                state = np.random.rand(20).astype(np.float32)
                action = np.random.randint(0, 10)
                reward = np.random.rand()
                done = np.random.rand() > 0.9
                
                episode["states"].append(state.tolist())
                episode["actions"].append(int(action))
                episode["rewards"].append(float(reward))
                episode["dones"].append(bool(done))
            
            episodes.append(episode)
        
        return episodes
    
    def generate_formation_control_data(
        self,
        num_samples: int = 5000
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Generate formation control training data.
        
        Args:
            num_samples: Number of samples
        
        Returns:
            Input states and target velocities
        """
        # Input: relative positions and velocities of neighbors
        X = np.random.randn(num_samples, 12).astype(np.float32)
        
        # Target: velocity commands that maintain formation
        y = np.zeros((num_samples, 2), dtype=np.float32)
        
        # Simple rule: move towards neighbor average
        for i in range(num_samples):
            neighbor_positions = X[i, :6].reshape(3, 2)
            center = neighbor_positions.mean(axis=0)
            y[i] = center * 0.1  # Soft attraction
        
        return X, y
    
    def generate_mission_planning_data(
        self,
        num_episodes: int = 1000
    ) -> List[Dict[str, Any]]:
        """Generate mission planning training data.
        
        Args:
            num_episodes: Number of episodes
        
        Returns:
            List of episodes
        """
        episodes = []
        
        for _ in range(num_episodes):
            episode = {
                "states": [],
                "actions": [],
                "rewards": []
            }
            
            num_steps = np.random.randint(5, 50)
            for _ in range(num_steps):
                # State: [current_pos, target_pos, threats, fuel]
                state = np.random.rand(10).astype(np.float32)
                # Action: waypoint selection (0-49)
                action = np.random.randint(0, 50)
                # Reward: based on progress towards target
                reward = 1.0 - np.linalg.norm(state[:2] - state[2:4])
                
                episode["states"].append(state.tolist())
                episode["actions"].append(int(action))
                episode["rewards"].append(float(reward))
            
            episodes.append(episode)
        
        return episodes
    
    def generate_workload_prediction_data(
        self,
        num_samples: int = 3000,
        seq_length: int = 30
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Generate workload prediction training data.
        
        Args:
            num_samples: Number of samples
            seq_length: Sequence length
        
        Returns:
            Sequences and labels
        """
        # Workload indicators: [active_missions, threat_level, fuel_status, battery, ...]
        X = np.random.rand(num_samples, seq_length, 10).astype(np.float32)
        
        # Labels: workload level (0-1)
        y = np.zeros(num_samples, dtype=np.float32)
        
        # High workload: many active missions, high threats, low battery
        for i in range(num_samples):
            avg_missions = X[i, :, 0].mean()
            avg_threats = X[i, :, 1].mean()
            avg_battery = X[i, :, 3].mean()
            
            workload = avg_missions * 0.4 + avg_threats * 0.4 + (1 - avg_battery) * 0.2
            y[i] = np.clip(workload, 0, 1)
        
        return X, y
    
    def save_dataset(self, name: str, X: np.ndarray, y: np.ndarray) -> None:
        """Save dataset to files.
        
        Args:
            name: Dataset name
            X: Features
            y: Labels
        """
        dataset_dir = self.data_dir / name
        dataset_dir.mkdir(parents=True, exist_ok=True)
        
        np.save(dataset_dir / "X.npy", X)
        np.save(dataset_dir / "y.npy", y)
    
    def save_episodes(self, name: str, episodes: List[Dict[str, Any]]) -> None:
        """Save episodes to JSON.
        
        Args:
            name: Dataset name
            episodes: Episodes list
        """
        dataset_dir = self.data_dir / name
        dataset_dir.mkdir(parents=True, exist_ok=True)
        
        with open(dataset_dir / "episodes.json", 'w') as f:
            json.dump(episodes, f)
