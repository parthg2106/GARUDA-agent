"""Configuration for advanced monitoring and observability."""

from pathlib import Path
from app.config import settings

# Logging configuration
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        },
        "json": {
            "format": '{"time": "%(asctime)s", "level": "%(levelname)s", "logger": "%(name)s", "message": "%(message)s"}'
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": settings.LOG_LEVEL,
            "formatter": settings.LOG_FORMAT,
            "stream": "ext://sys.stdout"
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": settings.LOG_LEVEL,
            "formatter": settings.LOG_FORMAT,
            "filename": f"{settings.TRAINING_OUTPUT_DIR}/garuda.log",
            "maxBytes": 10485760,  # 10MB
            "backupCount": 10
        }
    },
    "loggers": {
        "": {
            "level": settings.LOG_LEVEL,
            "handlers": ["console", "file"]
        }
    }
}

# Performance monitoring thresholds
PERFORMANCE_THRESHOLDS = {
    "max_latency_ms": 1000,
    "min_throughput_samples_per_sec": 10,
    "max_memory_usage_mb": 8000,
    "max_cpu_usage_percent": 90
}

# Model evaluation thresholds
MODEL_THRESHOLDS = {
    "threat_assessment": {
        "min_accuracy": 0.85,
        "max_loss": 0.3
    },
    "task_allocation": {
        "min_reward": -1.0,
        "max_loss": 0.5
    },
    "formation_control": {
        "min_convergence_rate": 0.8,
        "max_loss": 0.2
    },
    "mission_planning": {
        "min_success_rate": 0.7,
        "max_loss": 1.0
    },
    "workload_prediction": {
        "min_accuracy": 0.8,
        "max_loss": 0.25
    }
}

# Alert configuration
ALERTS = {
    "performance_degradation": {
        "enabled": True,
        "threshold": 0.2,  # 20% degradation
        "action": "log_warning"
    },
    "high_error_rate": {
        "enabled": True,
        "threshold": 0.05,  # 5% error rate
        "action": "log_error"
    },
    "model_drift": {
        "enabled": True,
        "threshold": 0.15,  # 15% drift
        "action": "trigger_retraining"
    }
}

# Feature extraction configuration for threat assessment
THREAT_FEATURES = {
    "distance_weight": 0.3,
    "drone_count_weight": 0.2,
    "altitude_weight": 0.15,
    "speed_weight": 0.2,
    "radar_signature_weight": 0.15
}

# Formation control parameters
FORMATION_PARAMS = {
    "cohesion_factor": 0.5,
    "separation_factor": 0.3,
    "alignment_factor": 0.2,
    "max_velocity": 100,
    "min_distance": 5
}

# Mission planning parameters
MISSION_PARAMS = {
    "planning_horizon": 50,
    "replanning_interval": 10,
    "contingency_buffer": 0.2,
    "fuel_reserve_percent": 15
}
