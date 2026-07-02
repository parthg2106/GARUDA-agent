"""Tests for GARUDA models."""

import pytest
import torch
import numpy as np
from models.threat_assessment import ThreatAssessmentModel
from models.task_allocation import TaskAllocationNetwork
from models.formation_control import FormationControlNetwork
from models.mission_planning import DQNAgent, ReplayBuffer
from models.workload_prediction import WorkloadPredictionLSTM


def test_threat_assessment_model():
    """Test threat assessment model."""
    model = ThreatAssessmentModel(input_size=5)
    
    # Test forward pass
    X = torch.randn(10, 5)
    output = model(X)
    
    assert output.shape == (10, 1)
    assert torch.all(output >= 0) and torch.all(output <= 1)  # Should be 0-1


def test_task_allocation_network():
    """Test task allocation network."""
    network = TaskAllocationNetwork(state_size=20, num_actions=10)
    
    # Test forward pass
    state = torch.randn(10, 20)
    action_logits, value = network(state)
    
    assert action_logits.shape == (10, 10)
    assert value.shape == (10, 1)


def test_formation_control_network():
    """Test formation control network."""
    model = FormationControlNetwork(input_size=12)
    
    # Test forward pass
    X = torch.randn(10, 12)
    velocities = model(X)
    
    assert velocities.shape == (10, 2)


def test_dqn_agent():
    """Test DQN agent."""
    agent = DQNAgent(state_size=10, num_actions=50)
    
    # Test action selection
    state = np.random.rand(10)
    action = agent.select_action(state, training=True)
    
    assert 0 <= action < 50
    
    # Test replay buffer
    agent.replay_buffer.add(state, action, 1.0, state, False)
    assert len(agent.replay_buffer) == 1


def test_workload_lstm():
    """Test workload prediction LSTM."""
    model = WorkloadPredictionLSTM(input_size=10, hidden_size=128)
    
    # Test forward pass
    X = torch.randn(10, 30, 10)  # Batch, seq_len, features
    output, hidden = model(X)
    
    assert output.shape == (10, 1)
    assert torch.all(output >= 0) and torch.all(output <= 1)  # Should be 0-1


def test_replay_buffer():
    """Test DQN replay buffer."""
    buffer = ReplayBuffer(max_size=100)
    
    # Add experiences
    for i in range(50):
        state = np.random.rand(10)
        action = i % 10
        reward = float(i)
        next_state = np.random.rand(10)
        done = i % 10 == 0
        
        buffer.add(state, action, reward, next_state, done)
    
    assert len(buffer) == 50
    
    # Sample batch
    batch = buffer.sample(10)
    assert len(batch) == 5  # states, actions, rewards, next_states, dones


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
