"""Threat analysis and assessment service."""

from typing import List, Dict, Any, Optional
import numpy as np
from app.utils.logger import logger
from app.utils.data_utils import calculate_distance, normalize_threat_level
from app.models.schemas import Mission, ThreatAssessment
import uuid
import time


class ThreatAnalyzer:
    """Analyzes threats and recommends countermeasures."""
    
    def __init__(self):
        self.threat_history: List[Dict[str, Any]] = []
        self.threat_models = {}
    
    def analyze(self, mission: Mission) -> List[ThreatAssessment]:
        """Analyze threats for a mission.
        
        Args:
            mission: Mission to analyze
        
        Returns:
            List of threat assessments
        """
        threats = []
        
        # Simulate threat detection
        if mission.threat_level is None:
            # Random threat level based on target location
            threat_value = np.random.rand() * 0.7 + 0.2  # 0.2-0.9
        else:
            threat_value = mission.threat_level
        
        if threat_value > 0.5:
            threat = ThreatAssessment(
                threat_id=str(uuid.uuid4()),
                threat_type="air_defense",
                location=mission.target_location,
                threat_level=normalize_threat_level(threat_value),
                recommended_action="evasive_maneuvers",
                timestamp=time.time()
            )
            threats.append(threat)
            logger.info(f"Threat detected for mission {mission.mission_id}: level={threat.threat_level}")
        
        self.threat_history.extend([t.dict() for t in threats])
        return threats
    
    def assess_threat(self, threat_data: Dict[str, Any]) -> ThreatAssessment:
        """Assess a specific threat.
        
        Args:
            threat_data: Threat data
        
        Returns:
            Threat assessment
        """
        threat_level = threat_data.get("threat_level", 0.5)
        
        # Determine recommended action based on threat level
        if threat_level > 0.7:
            action = "retreat"
        elif threat_level > 0.5:
            action = "evasive_maneuvers"
        else:
            action = "proceed_with_caution"
        
        assessment = ThreatAssessment(
            threat_id=str(uuid.uuid4()),
            threat_type=threat_data.get("threat_type", "unknown"),
            location=threat_data.get("location", [0, 0]),
            threat_level=normalize_threat_level(threat_level),
            recommended_action=action,
            timestamp=time.time()
        )
        
        logger.info(f"Threat assessed: {assessment.threat_id} - Action: {action}")
        return assessment
    
    def get_threat_summary(self) -> Dict[str, Any]:
        """Get threat analysis summary.
        
        Returns:
            Threat summary
        """
        if not self.threat_history:
            return {"threats_detected": 0, "average_threat_level": 0}
        
        threat_levels = [t["threat_level"] for t in self.threat_history]
        return {
            "threats_detected": len(self.threat_history),
            "average_threat_level": np.mean(threat_levels),
            "max_threat_level": np.max(threat_levels),
            "min_threat_level": np.min(threat_levels)
        }
