"""Setup and initialization script for GARUDA."""

import os
import sys
from pathlib import Path

def setup_directories():
    """Create necessary directories."""
    dirs = [
        "models",
        "logs",
        "checkpoints",
        "training_outputs",
        "training_outputs/datasets",
    ]
    
    for dir_path in dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        print(f"✓ Created directory: {dir_path}")

def create_env_file():
    """Create .env file if it doesn't exist."""
    env_content = """# GARUDA Environment Configuration
ENVIRONMENT=development
DEBUG=True
LOG_LEVEL=INFO
LOG_FORMAT=json

# Training
TRAINING_TIMESTEPS=1000000
BATCH_SIZE=64
LEARNING_RATE=0.0003
GAMMA=0.99

# Simulation
NUM_DRONES=4
GRID_SIZE=100
MAX_EPISODE_STEPS=500
"""
    
    if not Path(".env").exists():
        with open(".env", "w") as f:
            f.write(env_content)
        print("✓ Created .env file")
    else:
        print("✓ .env file already exists")

def check_dependencies():
    """Check if required packages are installed."""
    required_packages = [
        "torch",
        "fastapi",
        "pydantic",
        "numpy",
        "gymnasium",
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"✓ {package} is installed")
        except ImportError:
            missing.append(package)
            print(f"✗ {package} is NOT installed")
    
    if missing:
        print(f"\n⚠️  Missing packages: {', '.join(missing)}")
        print(f"Run: pip install {' '.join(missing)}")
        return False
    return True

def display_welcome():
    """Display welcome message."""
    print("""
    ╔═════════════════════════════════════════════════════════════════╗
    ║                                                                 ║
    ║              🚀 GARUDA - Autonomous Swarm Agent 🚀            ║
    ║                                                                 ║
    ║        Autonomous Swarm Coordination & Mission Execution       ║
    ║                                                                 ║
    ║                  Part of Project KRISHNA                       ║
    ║                                                                 ║
    ╚═════════════════════════════════════════════════════════════════╝
    """)

def main():
    """Run setup."""
    display_welcome()
    
    print("\n📋 Setting up GARUDA...\n")
    
    print("1️⃣  Creating directories...")
    setup_directories()
    
    print("\n2️⃣  Setting up environment...")
    create_env_file()
    
    print("\n3️⃣  Checking dependencies...")
    if not check_dependencies():
        print("\n⚠️  Please install missing dependencies and run setup again.")
        return False
    
    print("""
    ✅ Setup completed successfully!
    
    📚 Next steps:
    
    1. Start the API server:
       python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    
    2. View API documentation:
       Open http://localhost:8000/api/docs in your browser
    
    3. Train AI models:
       python training/train_models.py
    
    4. Run tests:
       pytest tests/ -v
    
    5. Deploy with Docker:
       docker-compose up --build
    
    📖 Documentation: https://github.com/parthg2106/GARUDA#readme
    
    """)
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
