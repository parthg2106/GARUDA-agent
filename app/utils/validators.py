"""Data validation utilities."""

from typing import Dict, List, Any
from app.config import MISSION_OBJECTIVES, DRONE_TYPES, FORMATION_TYPES


class ValidationError(Exception):
    """Validation error exception."""
    pass


def validate_mission(mission: Dict[str, Any]) -> bool:
    """Validate mission structure.
    
    Args:
        mission: Mission dictionary
    
    Returns:
        True if valid
    
    Raises:
        ValidationError: If validation fails
    """
    required_fields = ["mission_id", "objective", "priority", "target_location"]
    
    for field in required_fields:
        if field not in mission:
            raise ValidationError(f"Missing required field: {field}")
    
    if mission["objective"] not in MISSION_OBJECTIVES:
        raise ValidationError(f"Invalid objective: {mission['objective']}")
    
    if not isinstance(mission["priority"], (int, float)) or not 0 <= mission["priority"] <= 1:
        raise ValidationError("Priority must be between 0 and 1")
    
    if not isinstance(mission["target_location"], (list, tuple)) or len(mission["target_location"]) != 2:
        raise ValidationError("Target location must be [x, y] coordinates")
    
    return True


def validate_drone(drone: Dict[str, Any]) -> bool:
    """Validate drone structure.
    
    Args:
        drone: Drone dictionary
    
    Returns:
        True if valid
    
    Raises:
        ValidationError: If validation fails
    """
    required_fields = ["drone_id", "drone_type", "position", "battery_level"]
    
    for field in required_fields:
        if field not in drone:
            raise ValidationError(f"Missing required field: {field}")
    
    if drone["drone_type"] not in DRONE_TYPES:
        raise ValidationError(f"Invalid drone type: {drone['drone_type']}")
    
    if not isinstance(drone["position"], (list, tuple)) or len(drone["position"]) != 2:
        raise ValidationError("Position must be [x, y] coordinates")
    
    if not isinstance(drone["battery_level"], (int, float)) or not 0 <= drone["battery_level"] <= 100:
        raise ValidationError("Battery level must be between 0 and 100")
    
    return True


def validate_formation(formation: Dict[str, Any]) -> bool:
    """Validate formation structure.
    
    Args:
        formation: Formation dictionary
    
    Returns:
        True if valid
    
    Raises:
        ValidationError: If validation fails
    """
    required_fields = ["formation_id", "formation_type", "drone_ids", "center_position"]
    
    for field in required_fields:
        if field not in formation:
            raise ValidationError(f"Missing required field: {field}")
    
    if formation["formation_type"] not in FORMATION_TYPES:
        raise ValidationError(f"Invalid formation type: {formation['formation_type']}")
    
    if not isinstance(formation["drone_ids"], list) or len(formation["drone_ids"]) == 0:
        raise ValidationError("drone_ids must be a non-empty list")
    
    if not isinstance(formation["center_position"], (list, tuple)) or len(formation["center_position"]) != 2:
        raise ValidationError("Center position must be [x, y] coordinates")
    
    return True
