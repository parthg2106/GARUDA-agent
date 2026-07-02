"""Integration utilities for connecting with other KRISHNA agents."""

import aiohttp
import asyncio
from typing import Dict, Any, Optional
from app.utils.logger import logger
import json


class KRISHNAAgentClient:
    """Client for communicating with other Project KRISHNA agents."""
    
    def __init__(self, agent_registry: Dict[str, str] = None):
        """Initialize agent client.
        
        Args:
            agent_registry: Dictionary of agent_name -> agent_url
        """
        self.agent_registry = agent_registry or {}
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def __aenter__(self):
        """Async context manager entry."""
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.session:
            await self.session.close()
    
    def register_agent(self, agent_name: str, agent_url: str) -> None:
        """Register an agent.
        
        Args:
            agent_name: Agent name
            agent_url: Agent URL
        """
        self.agent_registry[agent_name] = agent_url
        logger.info(f"Registered agent: {agent_name} -> {agent_url}")
    
    async def send_request(
        self,
        agent_name: str,
        endpoint: str,
        method: str = "POST",
        data: Dict[str, Any] = None,
        timeout: int = 30
    ) -> Dict[str, Any]:
        """Send request to another agent.
        
        Args:
            agent_name: Target agent name
            endpoint: API endpoint
            method: HTTP method
            data: Request data
            timeout: Request timeout in seconds
        
        Returns:
            Response data
        """
        if agent_name not in self.agent_registry:
            logger.error(f"Agent not registered: {agent_name}")
            return {"error": f"Agent not found: {agent_name}"}
        
        agent_url = self.agent_registry[agent_name]
        url = f"{agent_url}{endpoint}"
        
        try:
            async with self.session.request(
                method,
                url,
                json=data,
                timeout=aiohttp.ClientTimeout(total=timeout)
            ) as response:
                result = await response.json()
                logger.info(f"Response from {agent_name}: {response.status}")
                return result
        except Exception as e:
            logger.error(f"Error communicating with {agent_name}: {str(e)}")
            return {"error": str(e)}
    
    async def broadcast_message(
        self,
        endpoint: str,
        data: Dict[str, Any],
        exclude_agents: list = None
    ) -> Dict[str, Dict[str, Any]]:
        """Broadcast message to all registered agents.
        
        Args:
            endpoint: API endpoint
            data: Message data
            exclude_agents: Agents to exclude
        
        Returns:
            Responses from all agents
        """
        if exclude_agents is None:
            exclude_agents = []
        
        responses = {}
        tasks = []
        
        for agent_name in self.agent_registry:
            if agent_name not in exclude_agents:
                task = self.send_request(agent_name, endpoint, data=data)
                tasks.append((agent_name, task))
        
        for agent_name, task in tasks:
            responses[agent_name] = await task
        
        return responses


class TacticalDataExchange:
    """Exchange tactical data with other agents."""
    
    @staticmethod
    def format_mission_briefing(mission: Dict[str, Any]) -> Dict[str, Any]:
        """Format mission data for inter-agent communication.
        
        Args:
            mission: Mission data
        
        Returns:
            Formatted mission briefing
        """
        return {
            "mission_id": mission.get("mission_id"),
            "objective": mission.get("objective"),
            "priority": mission.get("priority"),
            "target_location": mission.get("target_location"),
            "duration": mission.get("duration"),
            "threat_level": mission.get("threat_level"),
            "assigned_drones": mission.get("assigned_drones", [])
        }
    
    @staticmethod
    def format_threat_report(threats: list) -> Dict[str, Any]:
        """Format threat data for inter-agent communication.
        
        Args:
            threats: Threats list
        
        Returns:
            Formatted threat report
        """
        return {
            "threat_count": len(threats),
            "threats": [
                {
                    "threat_id": t.get("threat_id"),
                    "threat_type": t.get("threat_type"),
                    "location": t.get("location"),
                    "threat_level": t.get("threat_level"),
                    "recommended_action": t.get("recommended_action")
                }
                for t in threats
            ]
        }
    
    @staticmethod
    def format_swarm_status(drones: Dict[str, Any], formations: list) -> Dict[str, Any]:
        """Format swarm status for inter-agent communication.
        
        Args:
            drones: Drones dictionary
            formations: Formations list
        
        Returns:
            Formatted swarm status
        """
        return {
            "drone_count": len(drones),
            "drones": [
                {
                    "drone_id": drone_id,
                    "status": drone.get("status"),
                    "position": drone.get("position"),
                    "battery_level": drone.get("battery_level"),
                    "current_mission": drone.get("current_mission_id")
                }
                for drone_id, drone in drones.items()
            ],
            "formation_count": len(formations),
            "formations": [
                {
                    "formation_id": f.get("formation_id"),
                    "formation_type": f.get("formation_type"),
                    "drone_count": len(f.get("drone_ids", []))
                }
                for f in formations
            ]
        }
