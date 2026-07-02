"""README for GARUDA training and models."""

# GARUDA Training and Models

## Overview

This directory contains the complete training pipeline and AI models for GARUDA, the autonomous swarm coordination agent.

## Models

### 1. Threat Assessment Model
- **Type**: Supervised Learning (Feed-forward Neural Network)
- **Input**: [distance, drone_count, altitude, speed, radar_signature]
- **Output**: Threat level (0-1)
- **Training**: Classification with BCELoss
- **File**: `models/threat_assessment.py`

### 2. Task Allocation Model
- **Type**: Multi-Agent Reinforcement Learning (PPO)
- **Input**: Drone state (20 features)
- **Output**: Action probabilities + value estimate
- **Training**: Proximal Policy Optimization
- **File**: `models/task_allocation.py`

### 3. Formation Control Model
- **Type**: Supervised Learning (Feed-forward Neural Network)
- **Input**: Relative positions and velocities of neighbors (12 features)
- **Output**: Velocity commands [vx, vy]
- **Training**: MSE Loss
- **File**: `models/formation_control.py`

### 4. Mission Planning Model
- **Type**: Deep Reinforcement Learning (DQN)
- **Input**: Mission state (10 features)
- **Output**: Q-values for 50 waypoints
- **Training**: Temporal Difference Learning with replay buffer
- **File**: `models/mission_planning.py`

### 5. Workload Prediction Model
- **Type**: Recurrent Neural Network (LSTM)
- **Input**: Sequence of workload indicators (30 timesteps, 10 features each)
- **Output**: Pilot workload level (0-1)
- **Training**: Regression with BCELoss
- **File**: `models/workload_prediction.py`

## Training

### Running the Complete Training Pipeline

```bash
python training/train_models.py
```

This will:
1. Generate synthetic training data for all models
2. Train all 5 AI models
3. Save trained models to `models/` directory
4. Export training metrics

### Individual Model Training

```python
from training.train_models import TrainingPipeline

pipeline = TrainingPipeline()

# Train specific model
results = pipeline.train_threat_assessment(epochs=100)
results = pipeline.train_task_allocation(episodes=1000)
results = pipeline.train_formation_control(epochs=50)
results = pipeline.train_mission_planning(episodes=500)
results = pipeline.train_workload_prediction(epochs=100)
```

## Evaluation

### Running Model Evaluation

```bash
python training/evaluate.py
```

This evaluates:
- Threat assessment accuracy
- Formation control convergence
- Mission planning success in simulation

## Data Generation

Synthetic data is generated in `training/data_generation.py`:

```python
from training.data_generation import DataGenerator

gen = DataGenerator()

# Generate specific datasets
X, y = gen.generate_threat_assessment_data(num_samples=5000)
gen.save_dataset("threat_assessment", X, y)
```

## Simulation Environment

The `CombatSimulationEnv` in `models/simulation_env.py` provides an OpenAI Gymnasium-compatible environment for training and evaluation:

```python
from models.simulation_env import CombatSimulationEnv

env = CombatSimulationEnv(num_drones=4, grid_size=100)
obs, info = env.reset()

for _ in range(500):
    action = env.action_space.sample()  # Random action
    obs, reward, terminated, truncated, info = env.step(action)
    if terminated or truncated:
        break
```

## Testing

### Run All Tests

```bash
pytest tests/ -v
```

### Test Categories

- `tests/test_api.py`: API endpoint tests
- `tests/test_models.py`: Model unit tests

## Hardware Requirements

- GPU (CUDA 11.0+): For accelerated training
- CPU: 4+ cores recommended
- RAM: 8GB+ (16GB+ for large batch sizes)
- Storage: 10GB+ for models and datasets

## Performance Metrics

Training produces:
- Loss curves
- Validation metrics
- Model checkpoints
- Metrics summary JSON

## Configuration

Training parameters can be modified in `app/config.py`:

```python
TRAINING_TIMESTEPS = 1_000_000
BATCH_SIZE = 64
LEARNING_RATE = 3e-4
GAMMA = 0.99
```

## Future Improvements

- [ ] Integration with reinforcement learning frameworks (Stable-Baselines3)
- [ ] Distributed training on multiple GPUs
- [ ] Transfer learning from pre-trained models
- [ ] Multi-task learning
- [ ] Curriculum learning strategies
- [ ] Real-time model serving

## License

Part of Project KRISHNA
