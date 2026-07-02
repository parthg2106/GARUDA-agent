"""Data utilities and preprocessing."""

import numpy as np
from typing import Tuple, List, Dict, Any


def normalize_position(position: List[float], grid_size: int) -> np.ndarray:
    """Normalize position to [-1, 1] range.
    
    Args:
        position: [x, y] position
        grid_size: Grid size
    
    Returns:
        Normalized position
    """
    normalized = np.array(position) / (grid_size / 2) - 1
    return np.clip(normalized, -1, 1)


def denormalize_position(position: np.ndarray, grid_size: int) -> np.ndarray:
    """Denormalize position from [-1, 1] to grid coordinates.
    
    Args:
        position: Normalized position
        grid_size: Grid size
    
    Returns:
        Grid coordinates
    """
    return np.clip((position + 1) * (grid_size / 2), 0, grid_size)


def calculate_distance(pos1: List[float], pos2: List[float]) -> float:
    """Calculate Euclidean distance between two positions.
    
    Args:
        pos1: First position [x, y]
        pos2: Second position [x, y]
    
    Returns:
        Distance
    """
    return np.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)


def calculate_angle(pos1: List[float], pos2: List[float]) -> float:
    """Calculate angle between two positions.
    
    Args:
        pos1: First position [x, y]
        pos2: Second position [x, y]
    
    Returns:
        Angle in radians
    """
    dx = pos2[0] - pos1[0]
    dy = pos2[1] - pos1[1]
    return np.arctan2(dy, dx)


def normalize_threat_level(threat_value: float) -> float:
    """Normalize threat level to [0, 1].
    
    Args:
        threat_value: Raw threat value
    
    Returns:
        Normalized threat level
    """
    return np.clip(threat_value, 0, 1)


def softmax(values: np.ndarray) -> np.ndarray:
    """Compute softmax of values.
    
    Args:
        values: Input values
    
    Returns:
        Softmax probabilities
    """
    exp_values = np.exp(values - np.max(values))
    return exp_values / exp_values.sum()
