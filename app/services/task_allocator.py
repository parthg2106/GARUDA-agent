"""Task allocation and scheduling service."""

from typing import List, Dict, Any, Optional
import numpy as np
from app.utils.logger import logger
from app.utils.data_utils import calculate_distance, softmax
from app.models.schemas import Mission, DroneStatus, TaskAllocation, ThreatAssessment
import uuid


class TaskAllocator:
    """Allocates tasks to drones based on capabilities and availability."""
    
    def __init__(self):
        self.allocation_history: List[Dict[str, Any]] = []
    
    def allocate_tasks(
        self,
        mission: Mission,
        available_drones: Dict[str, DroneStatus],
        threats: List[ThreatAssessment]
    ) -> List[TaskAllocation]:
        """Allocate mission tasks to available drones.
        
        Args:
            mission: Mission to allocate
            available_drones: Available drones
            threats: Identified threats
        
        Returns:
            List of task allocations
        """
        allocations = []
        
        if not available_drones:
            logger.warning("No available drones for task allocation")
            return allocations
        
        # Calculate suitability scores for each drone
        drone_scores = self._calculate_drone_suitability(
            mission,
            available_drones,
            threats
        )
        
        # Select best drones
        selected_drones = self._select_drones(drone_scores, mission)
        
        # Create task allocations
        for i, drone_id in enumerate(selected_drones):
            task = TaskAllocation(
                task_id=str(uuid.uuid4()),
                mission_id=mission.mission_id,
                drone_id=drone_id,
                task_type="execute_mission",
                priority=mission.priority,
                estimated_completion_time=mission.duration or 300,
                success_probability=0.9
            )
            allocations.append(task)
        
        logger.info(f"Tasks allocated to {len(allocations)} drones for mission {mission.mission_id}")
        self.allocation_history.append({
            "mission_id": mission.mission_id,
            "drone_count": len(allocations),
            "allocations": [a.dict() for a in allocations]
        })
        
        return allocations
    
    def _calculate_drone_suitability(
        self,
        mission: Mission,
        available_drones: Dict[str, DroneStatus],
        threats: List[ThreatAssessment]
    ) -> Dict[str, float]:
        """Calculate suitability score for each drone.
        
        Args:
            mission: Mission
            available_drones: Available drones
            threats: Threats
        
        Returns:
            Dictionary of drone_id -> suitability_score
        """
        scores = {}
        
        for drone_id, drone in available_drones.items():
            # Distance score (closer is better)
            distance = calculate_distance(drone.position, mission.target_location)
            distance_score = max(0, 1 - distance / 100)
            
            # Battery score (higher is better)
            battery_score = drone.battery_level / 100
            
            # Combined score
            scores[drone_id] = (0.6 * distance_score) + (0.4 * battery_score)
        
        return scores
    
    def _select_drones(
        self,
        drone_scores: Dict[str, float],
        mission: Mission
    ) -> List[str]:
        """Select best drones for mission.
        
        Args:
            drone_scores: Drone suitability scores
            mission: Mission
        
        Returns:
            List of selected drone IDs
        """
        # Select top 2-4 drones based on mission priority
        num_drones = max(2, min(4, int(mission.priority * 4)))
        
        sorted_drones = sorted(
            drone_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        return [drone_id for drone_id, _ in sorted_drones[:num_drones]]
    
    def reallocate_tasks(
        self,
        mission_id: str,
        failed_drone: str,
        available_drones: Dict[str, DroneStatus]
    ) -> Optional[TaskAllocation]:
        """Reallocate task from failed drone to another drone.
        
        Args:
            mission_id: Mission ID
            failed_drone: Failed drone ID
            available_drones: Available drones
        
        Returns:
            New task allocation or None
        """
        logger.info(f"Reallocating task from failed drone {failed_drone}")
        
        # Find best replacement drone
        best_drone = max(
            available_drones.items(),
            key=lambda x: x[1].battery_level
        )[0]
        
        new_task = TaskAllocation(
            task_id=str(uuid.uuid4()),
            mission_id=mission_id,
            drone_id=best_drone,
            task_type="replacement_task",
            priority=0.9
        )
        
        logger.info(f"Task reallocated to drone {best_drone}")
        return new_task
