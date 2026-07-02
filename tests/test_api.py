"""Unit tests for GARUDA API endpoints."""

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models.schemas import Mission, DroneStatus, Formation, MissionObjectiveEnum, DroneTypeEnum, FormationTypeEnum

client = TestClient(app)


def test_health_check():
    """Test health check endpoint."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["version"] is not None


def test_root_endpoint():
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "GARUDA"
    assert data["status"] == "operational"


def test_register_drone():
    """Test drone registration."""
    drone_data = {
        "drone_id": "test_drone_001",
        "drone_type": "loyal_wingman",
        "position": [50, 50],
        "velocity": [0, 0],
        "battery_level": 85.5,
        "status": "operational"
    }
    
    response = client.post("/api/v1/drones/register", json=drone_data)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "registered"
    assert data["drone_id"] == "test_drone_001"


def test_execute_mission():
    """Test mission execution."""
    # Register a drone first
    drone_data = {
        "drone_id": "test_drone_002",
        "drone_type": "loyal_wingman",
        "position": [50, 50],
        "velocity": [0, 0],
        "battery_level": 100,
        "status": "operational"
    }
    client.post("/api/v1/drones/register", json=drone_data)
    
    # Execute mission
    mission_data = {
        "mission_id": "test_mission_001",
        "objective": "reconnaissance",
        "priority": 0.8,
        "target_location": [75, 75],
        "duration": 300
    }
    
    response = client.post("/api/v1/mission/execute", json=mission_data)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "accepted"
    assert data["mission_id"] is not None


def test_get_assets():
    """Test getting available assets."""
    response = client.get("/api/v1/assets")
    assert response.status_code == 200
    data = response.json()
    assert "drones" in data
    assert "formations" in data
    assert "missions" in data


def test_assign_formation():
    """Test swarm formation assignment."""
    formation_data = {
        "formation_id": "test_formation_001",
        "formation_type": "wedge",
        "drone_ids": ["drone_001", "drone_002", "drone_003"],
        "center_position": [50, 50],
        "spacing": 15.0
    }
    
    response = client.post("/api/v1/swarm/assign", json=formation_data)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "assigned"
    assert data["formation_id"] is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
