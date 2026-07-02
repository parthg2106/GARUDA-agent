"""Application configuration and constants."""

from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """Application settings."""
    
    # App
    APP_NAME: str = "GARUDA"
    APP_VERSION: str = "0.1.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # API
    API_V1_PREFIX: str = "/api/v1"
    API_TITLE: str = "GARUDA Autonomous Mission Execution Agent"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"
    
    # Models
    MODEL_DIR: str = "models"
    CHECKPOINT_DIR: str = "checkpoints"
    TRAINING_OUTPUT_DIR: str = "training_outputs"
    
    # Training
    TRAINING_TIMESTEPS: int = 1_000_000
    BATCH_SIZE: int = 64
    LEARNING_RATE: float = 3e-4
    GAMMA: float = 0.99
    
    # Simulation
    NUM_DRONES: int = 4
    GRID_SIZE: int = 100
    MAX_EPISODE_STEPS: int = 500
    
    # Threat Assessment
    THREAT_THRESHOLDS: dict = {
        "low": 0.33,
        "medium": 0.66,
        "high": 1.0
    }
    
    # Task Allocation
    ALLOCATION_TIMEOUT: int = 5
    REALLOCATION_INTERVAL: int = 10
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

# Mission constants
MISSION_OBJECTIVES = {
    "reconnaissance": 1,
    "interception": 2,
    "electronic_warfare": 3,
    "strike": 4,
    "defense": 5
}

DRONE_TYPES = {
    "loyal_wingman": "multi-role",
    "uav_recon": "reconnaissance",
    "ew_platform": "electronic_warfare",
    "decoy": "decoy",
    "strike_drone": "strike"
}

FORMATION_TYPES = {
    "wedge": "wedge",
    "line": "line",
    "triangle": "triangle",
    "circle": "circle",
    "scatter": "scatter"
}
