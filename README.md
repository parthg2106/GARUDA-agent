# GARUDA - Autonomous Swarm Coordination & Mission Execution Agent

![GARUDA](https://img.shields.io/badge/Project-KRISHNA-blue?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.11+-green?style=flat-square)
![PyTorch](https://img.shields.io/badge/PyTorch-2.1+-red?style=flat-square)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-blue?style=flat-square)

**GARUDA** is an autonomous mission execution agent for Project KRISHNA, designed to command AI-powered loyal wingman drones, optimize mission execution, and support fighter pilots with real-time tactical decision implementation in simulated combat environments.

## 🎯 Overview

GARUDA serves as the **execution layer** of the multi-agent combat intelligence ecosystem, converting high-level tactical recommendations into coordinated actions performed by autonomous aerial assets. The system manages heterogeneous autonomous assets including:

- 🚁 **Loyal Wingman Drones** - Multi-role autonomous fighters
- 🛫 **Reconnaissance UAVs** - Intelligence gathering
- ⚡ **Electronic Warfare Platforms** - Signal jamming and detection
- 🎯 **Strike Drones** - Precision engagement
- 🎪 **Decoy Drones** - Threat deception

## 🚀 Key Features

✅ **Multi-Agent AI Architecture** - Distributed decision-making across autonomous assets
✅ **Dynamic Mission Planning** - Real-time adaptation to battlefield conditions
✅ **Swarm Coordination** - Formation control and cooperative task execution
✅ **Threat-Aware Decision Engine** - Intelligent threat assessment and response
✅ **Real-Time Mission Replanning** - Contingency management and dynamic reassignment
✅ **Pilot Workload Reduction** - Automated decision support
✅ **REST API Interface** - JSON-based multi-agent communication
✅ **Production-Ready Deployment** - Docker containerization and scalability
✅ **Comprehensive AI Models** - Trained neural networks for mission execution
✅ **Simulation Environment** - Gymnasium-compatible training environment

## 📁 Project Structure

```
GARUDA/
├── app/
│   ├── api/
│   │   └── routes.py              # REST API endpoints
│   ├── services/
│   │   ├── mission_planner.py    # Mission planning logic
│   │   ├── threat_analyzer.py    # Threat assessment
│   │   └── task_allocator.py     # Task allocation to drones
│   ├── models/
│   │   └── schemas.py             # Pydantic data models
│   ├── utils/
│   │   ├── logger.py              # Structured logging
│   │   ├── metrics.py             # Metrics collection
│   │   ├── validators.py          # Data validation
│   │   └── data_utils.py          # Data utilities
│   ├── config.py                  # Configuration and constants
│   └── main.py                    # FastAPI application
│
├── models/
│   ├── threat_assessment.py       # Threat Assessment Model (DNN)
│   ├── task_allocation.py         # Task Allocation Model (PPO)
│   ├── formation_control.py       # Formation Control Model (DNN)
│   ├── mission_planning.py        # Mission Planning Model (DQN)
│   ├── workload_prediction.py     # Workload Prediction Model (LSTM)
│   └── simulation_env.py          # Combat Simulation Environment
│
├── training/
│   ├── data_generation.py         # Synthetic data generation
│   ├── train_models.py            # Training pipeline
│   ├── evaluate.py                # Model evaluation
│   └── README.md                  # Training documentation
│
├── tests/
│   ├── test_api.py                # API tests
│   └── test_models.py             # Model tests
│
├── requirements.txt               # Python dependencies
├── Dockerfile                     # Container configuration
├── docker-compose.yml             # Multi-container setup
├── .gitignore                     # Git ignore rules
└── README.md                      # This file
```

## 🏗️ Architecture

### AI Model Stack

| Model | Type | Purpose | Framework |
|-------|------|---------|───────────|
| **Threat Assessment** | Supervised DNN | Classify threat levels | PyTorch |
| **Task Allocation** | Multi-Agent RL (PPO) | Optimize drone task assignment | Stable-Baselines3 |
| **Formation Control** | Supervised DNN | Maintain coordinated formation | PyTorch |
| **Mission Planning** | Deep RL (DQN) | Optimal path planning | PyTorch |
| **Workload Prediction** | LSTM Sequence Model | Predict pilot workload | PyTorch |

### API Endpoints

```
POST   /api/v1/mission/execute        - Execute a new mission
POST   /api/v1/swarm/assign            - Assign drones to formation
POST   /api/v1/formation/update        - Update formation parameters
POST   /api/v1/threat/analyze          - Analyze and assess threats
POST   /api/v1/mission/replan          - Replan ongoing mission
GET    /api/v1/mission/status/{id}     - Get mission status
GET    /api/v1/assets                  - List available assets
GET    /api/v1/health                  - Health check
```

## ⚡ Quick Start

### Prerequisites

- Python 3.11+
- CUDA 11.0+ (optional, for GPU acceleration)
- Docker & Docker Compose (for containerized deployment)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/parthg2106/GARUDA.git
   cd GARUDA
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

#### Option 1: Local Development

```bash
# Start the FastAPI server
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

API documentation available at: `http://localhost:8000/api/docs`

#### Option 2: Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up --build
```

Access the API at: `http://localhost:8000`

### Training AI Models

```bash
# Run complete training pipeline
python training/train_models.py

# Evaluate trained models
python training/evaluate.py
```

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_api.py -v
```

## 📊 API Usage Examples

### 1. Register a Drone

```bash
curl -X POST http://localhost:8000/api/v1/drones/register \
  -H "Content-Type: application/json" \
  -d '{
    "drone_id": "drone_001",
    "drone_type": "loyal_wingman",
    "position": [50, 50],
    "battery_level": 100,
    "status": "operational"
  }'
```

### 2. Execute a Mission

```bash
curl -X POST http://localhost:8000/api/v1/mission/execute \
  -H "Content-Type: application/json" \
  -d '{
    "mission_id": "mission_001",
    "objective": "reconnaissance",
    "priority": 0.8,
    "target_location": [75, 75],
    "duration": 300
  }'
```

### 3. Assign Formation

```bash
curl -X POST http://localhost:8000/api/v1/swarm/assign \
  -H "Content-Type: application/json" \
  -d '{
    "formation_id": "formation_001",
    "formation_type": "wedge",
    "drone_ids": ["drone_001", "drone_002", "drone_003"],
    "center_position": [50, 50],
    "spacing": 15.0
  }'
```

### 4. Check Health

```bash
curl http://localhost:8000/api/v1/health
```

## 🤖 AI Models Training

### Threat Assessment Model
- **Input**: Distance, drone count, altitude, speed, radar signature
- **Output**: Threat level (0-1)
- **Training Data**: 5,000 synthetic samples
- **Architecture**: 3-layer DNN

### Task Allocation Model (PPO)
- **State**: 20-dimensional drone state vector
- **Actions**: 10 discrete task assignments
- **Training**: 1,000 episodes of policy optimization
- **Architecture**: Actor-Critic network

### Mission Planning Model (DQN)
- **State Space**: 10-dimensional mission features
- **Action Space**: 50 possible waypoints
- **Training**: 500 episodes with experience replay
- **Target Network**: Updated every 10 episodes

### Formation Control Model
- **Input**: Relative positions/velocities of neighbors
- **Output**: Velocity commands for cohesion
- **Loss Function**: MSE with smoothness penalty

### Workload Prediction Model (LSTM)
- **Input Sequence**: 30 timesteps of 10 workload indicators
- **Output**: Pilot workload prediction (0-1)
- **Architecture**: 2-layer LSTM with dense output

## 📈 Training Results

After running the training pipeline, results are saved to `training_outputs/`:

```
training_outputs/
├── training_metrics.json          # Summary metrics
├── datasets/
│   ├── threat_assessment/
│   ├── task_allocation/
│   ├── formation_control/
│   ├── mission_planning/
│   └── workload_prediction/
├── logs/
│   └── garuda.log                 # Training logs
└── checkpoints/
    └── *_best.pt / *_final.pt     # Model checkpoints
```

## 🔧 Configuration

Edit `app/config.py` to customize:

```python
# Training parameters
TRAINING_TIMESTEPS = 1_000_000
BATCH_SIZE = 64
LEARNING_RATE = 3e-4
GAMMA = 0.99

# Simulation environment
NUM_DRONES = 4
GRID_SIZE = 100
MAX_EPISODE_STEPS = 500

# Threat thresholds
THREAT_THRESHOLDS = {
    "low": 0.33,
    "medium": 0.66,
    "high": 1.0
}
```

## 📦 Dependencies

Key libraries used:

- **FastAPI** (0.104.1) - Web framework
- **PyTorch** (2.1.1) - Deep learning
- **Stable-Baselines3** (2.2.1) - RL algorithms
- **Gymnasium** (0.29.1) - Simulation environment
- **scikit-learn** (1.3.2) - Traditional ML
- **NumPy/Pandas** - Data processing

See `requirements.txt` for complete dependency list.

## 🧪 Testing

Comprehensive test suite included:

```bash
# API endpoint tests
pytest tests/test_api.py -v

# Model unit tests
pytest tests/test_models.py -v

# With coverage report
pytest tests/ --cov=app --cov=models --cov=training
```

## 🚀 Deployment

### Docker

```bash
# Build image
docker build -t garuda:latest .

# Run container
docker run -p 8000:8000 -v $(pwd)/logs:/app/logs garuda:latest
```

### Kubernetes (Helm)

```bash
# Coming soon: Helm charts for K8s deployment
```

## 📚 Documentation

- [Training Guide](training/README.md) - Detailed model training instructions
- [API Documentation](http://localhost:8000/api/docs) - Interactive Swagger UI
- [Model Architecture](docs/MODELS.md) - Detailed model descriptions (coming soon)
- [Performance Benchmarks](docs/BENCHMARKS.md) - Performance metrics (coming soon)

## 🔐 Security & Access

Full access and permissions enabled for development:

- ✅ Read/Write repository access
- ✅ Model checkpoint management
- ✅ Log and metrics export
- ✅ Configuration modification
- ✅ Test execution and CI/CD

## 🛣️ Roadmap

- [x] Core API infrastructure
- [x] AI model implementations
- [x] Training pipeline
- [x] Evaluation framework
- [x] Docker containerization
- [ ] Kubernetes deployment
- [ ] Real-time model serving (TensorRT)
- [ ] Multi-GPU training
- [ ] Reinforcement learning tuning
- [ ] Integration with digital twin
- [ ] Advanced visualization dashboard
- [ ] Hardware-in-the-loop testing

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

Part of **Project KRISHNA** - Multi-Agent Combat Intelligence Ecosystem

## 👥 Authors

**PARTH GHODKE** - Initial development

Project KRISHNA Team

## 🙏 Acknowledgments

- FastAPI community for the excellent framework
- PyTorch team for deep learning capabilities
- OpenAI Gym/Gymnasium for the simulation environment
- Stable-Baselines3 for RL implementations

## 📞 Support

For issues, questions, or suggestions:

1. Check existing [GitHub Issues](https://github.com/parthg2106/GARUDA/issues)
2. Create a new issue with detailed description
3. Submit a pull request with improvements

---

**GARUDA** - Autonomous Mission Execution for Next-Generation Combat Systems

*Part of Project KRISHNA: Multi-Agent Combat Intelligence Ecosystem*
