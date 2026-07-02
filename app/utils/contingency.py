"""Fallback and contingency handling."""

from typing import Dict, Any, List, Optional
from enum import Enum
from app.utils.logger import logger
import random


class ContingencyType(str, Enum):
    """Types of contingencies."""
    DRONE_LOSS = "drone_loss"
    COMMUNICATION_FAILURE = "communication_failure"
    HIGH_THREAT = "high_threat"
    FUEL_CRITICAL = "fuel_critical"
    MISSION_IMPOSSIBLE = "mission_impossible"


class ContingencyHandler:
    """Handles contingencies and fallback strategies."""
    
    def __init__(self):
        self.contingency_plans: Dict[ContingencyType, callable] = {}
        self.registered_plans: Dict[str, Dict[str, Any]] = {}
    
    def register_plan(
        self,
        contingency_type: ContingencyType,
        plan_name: str,
        plan_fn: callable
    ) -> None:
        """Register a contingency plan.
        
        Args:
            contingency_type: Type of contingency
            plan_name: Plan name
            plan_fn: Plan function
        """
        if contingency_type not in self.registered_plans:
            self.registered_plans[contingency_type] = {}
        
        self.registered_plans[contingency_type][plan_name] = plan_fn
        logger.info(f"Registered contingency plan: {plan_name} for {contingency_type}")
    
    def execute_plan(
        self,
        contingency_type: ContingencyType,
        plan_name: str,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute a contingency plan.
        
        Args:
            contingency_type: Type of contingency
            plan_name: Plan name
            context: Execution context
        
        Returns:
            Plan result
        """
        if contingency_type not in self.registered_plans:
            logger.error(f"No plans registered for: {contingency_type}")
            return {"status": "failed", "reason": "No plans available"}
        
        if plan_name not in self.registered_plans[contingency_type]:
            logger.error(f"Plan not found: {plan_name}")
            return {"status": "failed", "reason": "Plan not found"}
        
        plan_fn = self.registered_plans[contingency_type][plan_name]
        
        try:
            result = plan_fn(context)
            logger.info(f"Contingency plan executed: {plan_name}")
            return result
        except Exception as e:
            logger.error(f"Contingency plan failed: {str(e)}")
            return {"status": "failed", "reason": str(e)}
    
    def handle_drone_loss(
        self,
        lost_drone_id: str,
        mission_id: str,
        available_drones: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Handle loss of a drone.
        
        Args:
            lost_drone_id: ID of lost drone
            mission_id: Current mission ID
            available_drones: Available drones
        
        Returns:
            Contingency result
        """
        logger.warning(f"Drone lost: {lost_drone_id} during mission {mission_id}")
        
        # Find replacement drone
        replacement = None
        best_battery = -1
        
        for drone_id, drone in available_drones.items():
            if drone_id != lost_drone_id and drone.get("status") == "operational":
                battery = drone.get("battery_level", 0)
                if battery > best_battery:
                    best_battery = battery
                    replacement = drone_id
        
        if replacement:
            logger.info(f"Reassigned mission to replacement drone: {replacement}")
            return {
                "status": "handled",
                "action": "reassign",
                "replacement_drone": replacement
            }
        else:
            logger.warning("No replacement drone available")
            return {
                "status": "handled",
                "action": "abort_mission",
                "reason": "No replacement drone available"
            }
    
    def handle_high_threat(
        self,
        threat_level: float,
        mission_id: str
    ) -> Dict[str, Any]:
        """Handle high threat situation.
        
        Args:
            threat_level: Threat level (0-1)
            mission_id: Mission ID
        
        Returns:
            Contingency result
        """
        logger.warning(f"High threat detected: {threat_level:.2f} during mission {mission_id}")
        
        if threat_level > 0.9:
            return {
                "status": "handled",
                "action": "retreat",
                "return_to_base": True,
                "reason": "Extreme threat level"
            }
        elif threat_level > 0.7:
            return {
                "status": "handled",
                "action": "evasive_maneuvers",
                "formation_type": "scatter",
                "reason": "High threat detected"
            }
        else:
            return {
                "status": "handled",
                "action": "proceed_with_caution",
                "reason": "Moderate threat"
            }
    
    def handle_communication_failure(
        self,
        drones_affected: List[str],
        mission_id: str
    ) -> Dict[str, Any]:
        """Handle communication failure.
        
        Args:
            drones_affected: Affected drone IDs
            mission_id: Mission ID
        
        Returns:
            Contingency result
        """
        logger.error(f"Communication failure affecting {len(drones_affected)} drones")
        
        return {
            "status": "handled",
            "action": "autonomous_mode",
            "drones_affected": drones_affected,
            "fallback_behavior": "follow_last_orders",
            "retry_communication_interval": 5  # seconds
        }
    
    def handle_fuel_critical(
        self,
        drone_id: str,
        fuel_percent: float,
        current_location: List[float]
    ) -> Dict[str, Any]:
        """Handle critical fuel situation.
        
        Args:
            drone_id: Drone ID
            fuel_percent: Fuel percentage
            current_location: Current location
        
        Returns:
            Contingency result
        """
        logger.warning(f"Fuel critical for drone {drone_id}: {fuel_percent:.1f}%")
        
        return {
            "status": "handled",
            "action": "return_to_base",
            "drone_id": drone_id,
            "fuel_percent": fuel_percent,
            "priority": "high",
            "reason": "Fuel critically low"
        }
