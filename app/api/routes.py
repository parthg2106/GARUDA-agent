"""Main API routes."""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import List, Dict, Any
import uuid
import time
from app.models.schemas import (
    Mission, DroneStatus, Formation, MissionExecutionResponse,
    HealthResponse, ThreatAssessment, TaskAllocation
)
from app.utils.logger import logger
from app.services.mission_planner import MissionPlanner
from app.services.threat_analyzer import ThreatAnalyzer
from app.services.task_allocator import TaskAllocator
from app.config import settings

router = APIRouter(prefix=settings.API_V1_PREFIX, tags=["core"])

# Service instances
mission_planner = MissionPlanner()
threat_analyzer = ThreatAnalyzer()
task_allocator = TaskAllocator()

# In-memory storage (replace with database in production)
active_missions: Dict[str, Mission] = {}
active_drones: Dict[str, DroneStatus] = {}
active_formations: Dict[str, Formation] = {}
start_time = time.time()


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        version=settings.APP_VERSION,
        timestamp=time.time(),
        uptime=time.time() - start_time,
        active_missions=len(active_missions),
        active_drones=len(active_drones)
    )


@router.post("/mission/execute", response_model=MissionExecutionResponse)
async def execute_mission(
    mission: Mission,
    background_tasks: BackgroundTasks
) -> MissionExecutionResponse:
    """Execute a new mission.
    
    Args:
        mission: Mission to execute
        background_tasks: Background tasks
    
    Returns:
        Mission execution response
    """
    try:
        mission_id = mission.mission_id or str(uuid.uuid4())
        execution_id = str(uuid.uuid4())
        
        # Analyze threats
        threats = threat_analyzer.analyze(mission)
        logger.info(f"Threats identified for mission {mission_id}: {len(threats)}")
        
        # Allocate tasks
        allocations = task_allocator.allocate_tasks(
            mission,
            active_drones,
            threats
        )
        
        if not allocations:
            raise HTTPException(
                status_code=400,
                detail="No available drones for mission execution"
            )
        
        # Store mission
        mission.status = "executing"
        mission.assigned_drones = [a.drone_id for a in allocations]
        active_missions[mission_id] = mission
        
        logger.info(f"Mission {mission_id} execution started with {len(allocations)} drones")
        
        # Background execution
        background_tasks.add_task(
            mission_planner.execute_mission,
            mission_id,
            allocations
        )
        
        return MissionExecutionResponse(
            status="accepted",
            mission_id=mission_id,
            execution_id=execution_id,
            allocated_drones=mission.assigned_drones,
            estimated_completion_time=mission.duration or 300,
            success_probability=0.85,
            message="Mission accepted and execution initiated"
        )
    
    except Exception as e:
        logger.error(f"Mission execution failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/swarm/assign")
async def assign_swarm(formation: Formation) -> Dict[str, Any]:
    """Assign drones to a formation."""
    try:
        formation_id = formation.formation_id or str(uuid.uuid4())
        active_formations[formation_id] = formation
        
        logger.info(f"Formation {formation_id} assigned with {len(formation.drone_ids)} drones")
        
        return {
            "status": "assigned",
            "formation_id": formation_id,
            "drone_count": len(formation.drone_ids),
            "formation_type": formation.formation_type
        }
    
    except Exception as e:
        logger.error(f"Swarm assignment failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/formation/update")
async def update_formation(formation: Formation) -> Dict[str, Any]:
    """Update formation parameters."""
    try:
        formation_id = formation.formation_id
        if formation_id not in active_formations:
            raise HTTPException(status_code=404, detail="Formation not found")
        
        active_formations[formation_id] = formation
        logger.info(f"Formation {formation_id} updated")
        
        return {
            "status": "updated",
            "formation_id": formation_id,
            "center_position": formation.center_position,
            "spacing": formation.spacing
        }
    
    except Exception as e:
        logger.error(f"Formation update failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/threat/analyze", response_model=ThreatAssessment)
async def analyze_threat(threat_data: Dict[str, Any]) -> ThreatAssessment:
    """Analyze threat and recommend actions."""
    try:
        threat_assessment = threat_analyzer.assess_threat(threat_data)
        logger.info(f"Threat analyzed: {threat_assessment.threat_id}")
        return threat_assessment
    
    except Exception as e:
        logger.error(f"Threat analysis failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/mission/replan")
async def replan_mission(mission_id: str, new_objectives: Dict[str, Any]) -> Dict[str, Any]:
    """Replan an ongoing mission."""
    try:
        if mission_id not in active_missions:
            raise HTTPException(status_code=404, detail="Mission not found")
        
        mission = active_missions[mission_id]
        replanned_mission = mission_planner.replan_mission(mission, new_objectives)
        active_missions[mission_id] = replanned_mission
        
        logger.info(f"Mission {mission_id} replanned")
        
        return {
            "status": "replanned",
            "mission_id": mission_id,
            "message": "Mission objectives updated and replanning initiated"
        }
    
    except Exception as e:
        logger.error(f"Mission replan failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/mission/status/{mission_id}")
async def get_mission_status(mission_id: str) -> Dict[str, Any]:
    """Get current mission status."""
    if mission_id not in active_missions:
        raise HTTPException(status_code=404, detail="Mission not found")
    
    mission = active_missions[mission_id]
    return {
        "mission_id": mission_id,
        "objective": mission.objective,
        "status": mission.status,
        "assigned_drones": mission.assigned_drones,
        "priority": mission.priority,
        "target_location": mission.target_location
    }


@router.get("/assets")
async def get_assets() -> Dict[str, Any]:
    """Get available assets."""
    return {
        "drones": len(active_drones),
        "formations": len(active_formations),
        "missions": len(active_missions),
        "drone_list": list(active_drones.keys()),
        "formation_list": list(active_formations.keys())
    }


@router.post("/drones/register")
async def register_drone(drone: DroneStatus) -> Dict[str, Any]:
    """Register a new drone."""
    try:
        drone_id = drone.drone_id
        active_drones[drone_id] = drone
        logger.info(f"Drone {drone_id} registered")
        
        return {
            "status": "registered",
            "drone_id": drone_id,
            "drone_type": drone.drone_type,
            "battery_level": drone.battery_level
        }
    
    except Exception as e:
        logger.error(f"Drone registration failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/drones/{drone_id}")
async def get_drone_status(drone_id: str) -> DroneStatus:
    """Get drone status."""
    if drone_id not in active_drones:
        raise HTTPException(status_code=404, detail="Drone not found")
    return active_drones[drone_id]
