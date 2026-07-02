"""Simulation environment for training GARUDA."""

import gymnasium as gym
from gymnasium import spaces
import numpy as np
from typing import Tuple, Dict, Any
from app.config import settings
from app.utils.logger import logger


class CombatSimulationEnv(gym.Env):
    """OpenAI Gymnasium environment for combat simulation.
    
    Agents must coordinate to complete missions while avoiding threats.
    """
    
    def __init__(
        self,
        num_drones: int = settings.NUM_DRONES,
        grid_size: int = settings.GRID_SIZE,
        max_steps: int = settings.MAX_EPISODE_STEPS
    ):
        super(CombatSimulationEnv, self).__init__()
        
        self.num_drones = num_drones
        self.grid_size = grid_size
        self.max_steps = max_steps
        self.current_step = 0
        
        # State space: position, velocity, battery for each drone + threats
        self.observation_space = spaces.Box(
            low=-1, high=1,
            shape=(num_drones * 5 + 10,),  # drones (5 features each) + threats
            dtype=np.float32
        )
        
        # Action space: velocity commands for each drone
        self.action_space = spaces.Box(
            low=-1, high=1,
            shape=(num_drones * 2,),  # [vx, vy] for each drone
            dtype=np.float32
        )
        
        # Initialize state
        self.drone_positions = np.random.rand(num_drones, 2) * grid_size
        self.drone_velocities = np.zeros((num_drones, 2))
        self.drone_battery = np.ones(num_drones) * 100
        self.target_location = np.random.rand(2) * grid_size
        self.threats = []
        self.mission_complete = False
    
    def _generate_observation(self) -> np.ndarray:
        """Generate observation from current state.
        
        Returns:
            Observation array
        """
        obs = []
        
        # Drone states (normalized)
        for i in range(self.num_drones):
            pos_norm = self.drone_positions[i] / self.grid_size
            vel_norm = np.clip(self.drone_velocities[i] / 10, -1, 1)
            battery_norm = self.drone_battery[i] / 100
            obs.extend(list(pos_norm) + list(vel_norm) + [battery_norm])
        
        # Target location (normalized)
        target_norm = self.target_location / self.grid_size
        obs.extend(list(target_norm))
        
        # Threat indicators (simplified)
        threat_indicator = min(len(self.threats), 5)  # Up to 5 threats
        obs.extend([0] * (10 - len(target_norm) - threat_indicator))
        
        return np.array(obs, dtype=np.float32)
    
    def _calculate_reward(self) -> float:
        """Calculate reward for current step.
        
        Returns:
            Reward value
        """
        reward = 0.0
        
        # Distance to target (negative reward for distance)
        avg_distance = np.mean([
            np.linalg.norm(pos - self.target_location)
            for pos in self.drone_positions
        ])
        reward -= avg_distance / self.grid_size
        
        # Formation bonus (drones staying close together)
        if self.num_drones > 1:
            pairwise_distances = []
            for i in range(self.num_drones):
                for j in range(i + 1, self.num_drones):
                    dist = np.linalg.norm(self.drone_positions[i] - self.drone_positions[j])
                    pairwise_distances.append(dist)
            
            avg_pair_distance = np.mean(pairwise_distances)
            formation_bonus = max(0, 1 - avg_pair_distance / 30)
            reward += formation_bonus * 0.1
        
        # Threat penalty
        threat_penalty = len(self.threats) * 0.1
        reward -= threat_penalty
        
        # Battery drain penalty
        battery_penalty = np.mean(100 - self.drone_battery) / 100 * 0.1
        reward -= battery_penalty
        
        # Mission completion bonus
        if self.mission_complete:
            reward += 10.0
        
        return reward
    
    def step(self, action: np.ndarray) -> Tuple[np.ndarray, float, bool, bool, Dict[str, Any]]:
        """Execute one step of the environment.
        
        Args:
            action: Action array
        
        Returns:
            Observation, reward, terminated, truncated, info
        """
        self.current_step += 1
        
        # Apply actions (velocity commands)
        for i in range(self.num_drones):
            self.drone_velocities[i] = action[i*2:(i+1)*2]
        
        # Update positions
        self.drone_positions += self.drone_velocities * 0.1
        self.drone_positions = np.clip(self.drone_positions, 0, self.grid_size)
        
        # Drain battery
        self.drone_battery -= np.linalg.norm(self.drone_velocities, axis=1) * 0.5
        self.drone_battery = np.clip(self.drone_battery, 0, 100)
        
        # Check mission completion
        avg_distance = np.mean([
            np.linalg.norm(pos - self.target_location)
            for pos in self.drone_positions
        ])
        self.mission_complete = avg_distance < 5.0
        
        # Generate threats (randomly)
        if np.random.rand() < 0.1:
            self.threats.append({
                "location": np.random.rand(2) * self.grid_size,
                "level": np.random.rand()
            })
        
        # Remove old threats
        self.threats = self.threats[-5:]
        
        # Calculate reward
        reward = self._calculate_reward()
        
        # Check termination
        terminated = self.mission_complete or np.any(self.drone_battery < 10)
        truncated = self.current_step >= self.max_steps
        
        observation = self._generate_observation()
        info = {
            "mission_complete": self.mission_complete,
            "avg_distance": avg_distance,
            "drone_count": self.num_drones,
            "threats": len(self.threats)
        }
        
        return observation, reward, terminated, truncated, info
    
    def reset(self, seed: int = None) -> Tuple[np.ndarray, Dict[str, Any]]:
        """Reset environment to initial state.
        
        Args:
            seed: Random seed
        
        Returns:
            Initial observation and info
        """
        super().reset(seed=seed)
        
        self.current_step = 0
        self.drone_positions = np.random.rand(self.num_drones, 2) * self.grid_size
        self.drone_velocities = np.zeros((self.num_drones, 2))
        self.drone_battery = np.ones(self.num_drones) * 100
        self.target_location = np.random.rand(2) * self.grid_size
        self.threats = []
        self.mission_complete = False
        
        observation = self._generate_observation()
        info = {}
        
        return observation, info
    
    def render(self, mode: str = 'human') -> None:
        """Render environment.
        
        Args:
            mode: Render mode
        """
        pass  # Implement visualization if needed
