# GARUDA - Autonomous Swarm Coordination & Mission Execution Agent

![GARUDA](https://img.shields.io/badge/Project-KRISHNA-blue?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.11+-green?style=flat-square)
![PyTorch](https://img.shields.io/badge/PyTorch-2.1+-red?style=flat-square)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-blue?style=flat-square)
![React](https://img.shields.io/badge/React-18.0+-blue?style=flat-square)

**GARUDA** is an autonomous mission execution agent for Project KRISHNA, designed to command AI-powered loyal wingman drones, optimize mission execution, and support fighter pilots with real-time tactical decision support through an intuitive web dashboard.

## 🎯 Overview

GARUDA serves as the **execution layer** of the multi-agent combat intelligence ecosystem, converting high-level tactical recommendations into coordinated actions performed by autonomous aerial assets. It features a modern, responsive web dashboard for mission planning, real-time drone monitoring, and tactical visualization.

### Autonomous Assets
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
✅ **Interactive Web Dashboard** - Real-time mission visualization and control
✅ **Responsive UI/UX** - Modern design for tactical decision-making

## 📁 Project Structure

```
GARUDA/
├── frontend/                           # React web dashboard
│   ├── src/
│   │   ├── components/
│   │   │   ├── Dashboard.jsx          # Main dashboard
│   │   │   ├── MissionPlanner.jsx     # Mission planning UI
│   │   │   ├── DroneMonitor.jsx       # Real-time drone tracking
│   │   │   ├── ThreatAssessment.jsx   # Threat visualization
│   │   │   ├── FormationControl.jsx   # Formation management
│   │   │   ├── Sidebar.jsx            # Navigation sidebar
│   │   │   └── MapViewer.jsx          # 3D/2D map visualization
│   │   ├── pages/
│   │   │   ├── Home.jsx
│   │   │   ├── Missions.jsx
│   │   │   ├── Drones.jsx
│   │   │   └── Analytics.jsx
│   │   ├── services/
│   │   │   └── api.js                 # API client
│   │   ├── styles/
│   │   │   ├── dashboard.css
│   │   │   ├── mission-planner.css
│   │   │   └── globals.css
│   │   ├── App.jsx
│   │   └── index.js
│   ├── public/
│   │   └── index.html
│   ├── package.json
│   └── README.md
│
├── app/
│   ├── api/
│   │   └── routes.py                  # REST API endpoints
│   ├── services/
│   │   ├── mission_planner.py        # Mission planning logic
│   │   ├── threat_analyzer.py        # Threat assessment
│   │   └── task_allocator.py         # Task allocation to drones
│   ├── models/
│   │   └── schemas.py                 # Pydantic data models
│   ├── utils/
│   │   ├── logger.py                  # Structured logging
│   │   ├── metrics.py                 # Metrics collection
│   │   ├── validators.py              # Data validation
│   │   └── data_utils.py              # Data utilities
│   ├── config.py                      # Configuration and constants
│   └── main.py                        # FastAPI application
│
├── models/
│   ├── threat_assessment.py           # Threat Assessment Model (DNN)
│   ├── task_allocation.py             # Task Allocation Model (PPO)
│   ├── formation_control.py           # Formation Control Model (DNN)
│   ├── mission_planning.py            # Mission Planning Model (DQN)
│   ├── workload_prediction.py         # Workload Prediction Model (LSTM)
│   └── simulation_env.py              # Combat Simulation Environment
│
├── training/
│   ├── data_generation.py             # Synthetic data generation
│   ├── train_models.py                # Training pipeline
│   ├── evaluate.py                    # Model evaluation
│   └── README.md                      # Training documentation
│
├── tests/
│   ├── test_api.py                    # API tests
│   └── test_models.py                 # Model tests
│
├── requirements.txt                   # Python dependencies
├── Dockerfile                         # Container configuration
├── docker-compose.yml                 # Multi-container setup
├── .gitignore                         # Git ignore rules
└── README.md                          # This file
```

## 🏗️ Architecture

### AI Model Stack

| Model | Type | Purpose | Framework |
|-------|------|---------|-----------|
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

### Frontend Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Framework** | React 18+ | UI library |
| **Styling** | CSS3 + Tailwind | Responsive design |
| **Maps** | Mapbox/Leaflet | Tactical visualization |
| **Charts** | Chart.js/D3.js | Data visualization |
| **State** | Redux/Context | State management |
| **HTTP** | Axios/Fetch | API communication |
| **Build** | Vite/Webpack | Module bundler |

### UI/UX Design

#### Key Dashboard Features
- **Real-Time Mission Status** - Live drone positions and status indicators
- **Threat Heatmap** - Visual threat level assessment
- **Formation Visualization** - 3D/2D drone formation display
- **Mission Timeline** - Chronological mission events
- **Pilot Workload Indicator** - Real-time workload metrics
- **Quick Actions Panel** - One-click mission controls
- **Analytics Dashboard** - Performance metrics and trends

#### Design Principles
- **Minimal & Clean** - Reduce cognitive load for tactical situations
- **Dark Mode** - Eye-friendly for extended use
- **High Contrast** - Accessibility for critical information
- **Responsive** - Works on desktop, tablet, and mobile
- **Accessibility** - WCAG 2.1 AA compliant
- **Real-Time Updates** - WebSocket integration for live data

## ⚡ Quick Start Guide (Windows/Mac/Linux)

### Prerequisites

- **Python** 3.11+
- **Node.js** 16+ (for frontend)
- **Git**
- **Optional**: Docker & Docker Compose

### Installation Steps

#### 1️⃣ Clone the Repository

```bash
git clone https://github.com/parthg2106/GARUDA-agent.git
cd GARUDA-agent
```

#### 2️⃣ Backend Setup (Python)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

#### 3️⃣ Frontend Setup (React)

```bash
# Navigate to frontend directory
cd frontend

# Install Node dependencies
npm install

# Navigate back to root
cd ..
```

#### 4️⃣ Configure Environment

Create a `.env` file in the root directory:

```env
# Backend Configuration
BACKEND_URL=http://localhost:8000
FASTAPI_ENV=development
LOG_LEVEL=INFO

# Frontend Configuration
REACT_APP_API_URL=http://localhost:8000/api/v1
REACT_APP_WS_URL=ws://localhost:8000/ws

# Database (optional)
DATABASE_URL=sqlite:///./garuda.db

# GPU/CUDA (optional)
CUDA_VISIBLE_DEVICES=0
```

### Running the Application

#### Option 1: Local Development (Recommended for Beginners)

**Terminal 1 - Start Backend:**
```bash
# Activate virtual environment first
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Start the FastAPI server
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Backend will be available at: `http://localhost:8000`
API docs: `http://localhost:8000/api/docs`

**Terminal 2 - Start Frontend:**
```bash
cd frontend
npm start
```

Frontend will be available at: `http://localhost:3000`

#### Option 2: Docker Deployment (Recommended for Production)

```bash
# Build and run with Docker Compose
docker-compose up --build

# Services will be available at:
# - Frontend: http://localhost:3000
# - Backend: http://localhost:8000
# - API Docs: http://localhost:8000/api/docs
```

To stop services:
```bash
docker-compose down
```

### Training AI Models

```bash
# Activate virtual environment
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Run complete training pipeline
python training/train_models.py

# Evaluate trained models
python training/evaluate.py

# Expected output in training_outputs/ directory
```

### Running Tests

```bash
# Activate virtual environment
source venv/bin/activate

# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_api.py -v

# Run with coverage report
pytest tests/ --cov=app --cov=models --cov=training
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
├── training_metrics.json              # Summary metrics
├── datasets/
│   ├── threat_assessment/
│   ├── task_allocation/
│   ├── formation_control/
│   ├── mission_planning/
│   └── workload_prediction/
├── logs/
│   └── garuda.log                     # Training logs
└── checkpoints/
    └── *_best.pt / *_final.pt         # Model checkpoints
```

## 🎨 Frontend Development

### Frontend Prerequisites

- Node.js 16+
- npm or yarn

### Frontend Dependencies

- React 18+
- React Router v6
- Axios for API calls
- Tailwind CSS or Material-UI
- Mapbox GL JS for mapping
- Chart.js for visualization
- WebSocket API for real-time updates

### Frontend Development Commands

```bash
cd frontend

# Start development server
npm start

# Build for production
npm run build

# Run tests
npm test

# Run linting
npm run lint
```

### UI Components Overview

```
Dashboard/
├── Header
│   ├── Logo
│   ├── Navigation
│   └── Status Indicators
├── Sidebar
│   ├── Mission Nav
│   ├── Drone Status
│   └── Quick Actions
├── Main Content
│   ├── Map Viewer
│   │   ├── Drone Markers
│   │   ├── Mission Path
│   │   └── Threat Zones
│   ├── Metrics Panel
│   │   ├── Drone Health
│   │   ├── Mission Progress
│   │   └── Resource Usage
│   └── Control Panel
│       ├── Mission Commands
│       ├── Formation Controls
│       └── Emergency Actions
└── Footer
    ├── System Status
    └── Logs/Events
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

# Frontend configuration
FRONTEND_URL = "http://localhost:3000"
CORS_ORIGINS = ["http://localhost:3000", "http://localhost:8000"]
```

## 📦 Dependencies

### Backend Dependencies
- **FastAPI** (0.104.1) - Web framework
- **PyTorch** (2.1.1) - Deep learning
- **Stable-Baselines3** (2.2.1) - RL algorithms
- **Gymnasium** (0.29.1) - Simulation environment
- **scikit-learn** (1.3.2) - Traditional ML
- **NumPy/Pandas** - Data processing

### Frontend Dependencies
- **React** (18.0+) - UI library
- **React Router** (6.0+) - Navigation
- **Axios** (1.0+) - HTTP client
- **Tailwind CSS** (3.0+) - Styling
- **Mapbox GL JS** (2.0+) - Mapping
- **Chart.js** (4.0+) - Visualization

See `requirements.txt` and `frontend/package.json` for complete dependency lists.

## 🧪 Testing

Comprehensive test suite included:

```bash
# Backend API endpoint tests
pytest tests/test_api.py -v

# Backend model unit tests
pytest tests/test_models.py -v

# With coverage report
pytest tests/ --cov=app --cov=models --cov=training

# Frontend tests (if configured)
cd frontend && npm test
```

## 🚀 Deployment

### Docker

```bash
# Build image
docker build -t garuda:latest .

# Run container
docker run -p 8000:8000 -p 3000:3000 -v $(pwd)/logs:/app/logs garuda:latest
```

### Docker Compose

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down
```

### Kubernetes (Future)
```bash
# Coming soon: Helm charts for K8s deployment
```

## 📚 Documentation

- [Training Guide](training/README.md) - Detailed model training instructions
- [API Documentation](http://localhost:8000/api/docs) - Interactive Swagger UI
- [Frontend README](frontend/README.md) - UI/UX development guide
- [Model Architecture](docs/MODELS.md) - Detailed model descriptions (coming soon)
- [Performance Benchmarks](docs/BENCHMARKS.md) - Performance metrics (coming soon)
- [Deployment Guide](docs/DEPLOYMENT.md) - Production deployment (coming soon)

## 🔐 Security & Access

Full access and permissions enabled for development:

- ✅ Read/Write repository access
- ✅ Model checkpoint management
- ✅ Log and metrics export
- ✅ Configuration modification
- ✅ Test execution and CI/CD
- ✅ Frontend asset management
- ✅ WebSocket connections for real-time data

## 🛣️ Roadmap

### Backend
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

### Frontend
- [ ] Interactive mission planning UI
- [ ] Real-time drone tracking dashboard
- [ ] 3D map visualization
- [ ] Advanced threat visualization
- [ ] Formation control interface
- [ ] Analytics and reporting dashboard
- [ ] Mobile responsive design
- [ ] Dark/Light theme toggle
- [ ] Voice command integration
- [ ] AR/VR visualization support

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup
- Follow the Quick Start Guide above
- Create feature branches from `develop`
- Ensure tests pass before submitting PR
- Update documentation as needed

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
- React community for frontend capabilities
- Mapbox and chart.js for visualization libraries

## 📞 Support

For issues, questions, or suggestions:

1. Check existing [GitHub Issues](https://github.com/parthg2106/GARUDA-agent/issues)
2. Create a new issue with detailed description
3. Submit a pull request with improvements
4. Check [Discussions](https://github.com/parthg2106/GARUDA-agent/discussions) for Q&A

## 🎓 Getting Started Checklist

- [ ] Clone repository
- [ ] Create Python virtual environment
- [ ] Install Python dependencies
- [ ] Install Node.js dependencies (frontend)
- [ ] Create `.env` file
- [ ] Start backend server
- [ ] Start frontend development server
- [ ] Access dashboard at http://localhost:3000
- [ ] Review API docs at http://localhost:8000/api/docs
- [ ] Run tests to verify setup
- [ ] Train models (optional)

---

**GARUDA** - Autonomous Mission Execution for Next-Generation Combat Systems

*Part of Project KRISHNA: Multi-Agent Combat Intelligence Ecosystem*
