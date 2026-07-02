"""Pydantic schemas for API requests/responses."""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from enum import Enum


class DroneTypeEnum(str, Enum):
    """Drone types."""
    LOYAL_WINGMAN = "loyal_wingman"
    UAV_RECON = "uav_recon"
    EW_PLATFORM = "ew_platform"
    DECOY = "decoy"
    STRIKE_DRONE = "strike_drone"


class MissionObjectiveEnum(str, Enum):
    """Mission objectives."""
    RECONNAISSANCE = "reconnaissance"
    INTERCEPTION = "interception"
    ELECTRONIC_WARFARE = "electronic_warfare"
    STRIKE = "strike"
    DEFENSE = "defense"


class FormationTypeEnum(str, Enum):
    """Formation types."""
    WEDGE = "wedge"
    LINE = "line"
    TRIANGLE = "triangle"
    CIRCLE = "circle"
    SCATTER = "scatter"


class DroneStatus(BaseModel):
    """Drone status model."""
    drone_id: str
    drone_type: DroneTypeEnum
    position: List[float] = Field(..., description="[x, y] coordinates")
    velocity: List[float] = Field(default=[0, 0], description="[vx, vy]")
    battery_level: float = Field(..., ge=0, le=100)
    status: str = Field(default="operational")
    current_mission_id: Optional[str] = None
    fuel_remaining: Optional[float] = None
    sensors_active: bool = Field(default=True)
    
    class Config:
        json_schema_extra = {
            "example": {
                "drone_id": "drone_001",
                "drone_type": "loyal_wingman",
                "position": [50, 50],
                "velocity": [5, 0],
                "battery_level": 85.5,
                "status": "operational"
            }
        }


class Mission(BaseModel):
    """Mission model."""
    mission_id: str
    objective: MissionObjectiveEnum
    priority: float = Field(..., ge=0, le=1)
    target_location: List[float] = Field(..., description="[x, y] coordinates")
    duration: Optional[int] = None
    assigned_drones: List[str] = Field(default=[])
    status: str = Field(default="pending")
    threat_level: Optional[float] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "mission_id": "mission_001",
                "objective": "reconnaissance",
                "priority": 0.8,
                "target_location": [75, 75],
                "duration": 300
            }
        }


class Formation(BaseModel):
    """Formation model."""
    formation_id: str
    formation_type: FormationTypeEnum
    drone_ids: List[str]
    center_position: List[float] = Field(..., description="[x, y] coordinates")
    spacing: float = Field(default=10.0)
    active: bool = Field(default=True)
    
    class Config:
        json_schema_extra = {
            "example": {
                "formation_id": "formation_001",
                "formation_type": "wedge",
                "drone_ids": ["drone_001", "drone_002", "drone_003"],
                "center_position": [50, 50],
                "spacing": 15.0
            }
        }


class ThreatAssessment(BaseModel):
    """Threat assessment model."""
    threat_id: str
    threat_type: str
    location: List[float]
    threat_level: float = Field(..., ge=0, le=1)
    affected_drones: List[str] = Field(default=[])
    recommended_action: str
    timestamp: float
    
    class Config:
        json_schema_extra = {
            "example": {
                "threat_id": "threat_001",
                "threat_type": "air_defense",
                "location": [60, 60],
                "threat_level": 0.8,
                "recommended_action": "evade"
            }
        }


class TaskAllocation(BaseModel):
    """Task allocation model."""
    task_id: str
    mission_id: str
    drone_id: str
    task_type: str
    priority: float
    estimated_completion_time: Optional[int] = None
    success_probability: float = Field(default=0.9, ge=0, le=1)
    
    class Config:
        json_schema_extra = {
            "example": {
                "task_id": "task_001",
                "mission_id": "mission_001",
                "drone_id": "drone_001",
                "task_type": "scout",
                "priority": 0.9
            }
        }


class MissionExecutionResponse(BaseModel):
    """Mission execution response."""
    status: str
    mission_id: str
    execution_id: str
    allocated_drones: List[str]
    estimated_completion_time: int
    success_probability: float
    message: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "accepted",
                "mission_id": "mission_001",
                "execution_id": "exec_001",
                "allocated_drones": ["drone_001", "drone_002"],
                "estimated_completion_time": 300,
                "success_probability": 0.95,
                "message": "Mission accepted and execution initiated"
            }
        }


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    version: str
    timestamp: float
    uptime: float
    active_missions: int
    active_drones: int
