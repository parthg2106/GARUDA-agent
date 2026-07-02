"""Monitoring and health check utilities."""

import time
import psutil
from typing import Dict, Any
from datetime import datetime
from app.utils.logger import logger


class SystemMonitor:
    """Monitors system resources and health."""
    
    def __init__(self):
        self.start_time = time.time()
        self.initial_process = psutil.Process()
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get current system status.
        
        Returns:
            System status dictionary
        """
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            process = psutil.Process()
            process_memory = process.memory_info().rss / (1024 * 1024)  # MB
            process_cpu = process.cpu_percent(interval=1)
            
            return {
                "timestamp": datetime.utcnow().isoformat(),
                "uptime_seconds": time.time() - self.start_time,
                "system": {
                    "cpu_percent": cpu_percent,
                    "memory_percent": memory.percent,
                    "memory_available_mb": memory.available / (1024 * 1024),
                    "disk_percent": disk.percent
                },
                "process": {
                    "memory_mb": process_memory,
                    "cpu_percent": process_cpu,
                    "num_threads": process.num_threads()
                }
            }
        except Exception as e:
            logger.error(f"Error getting system status: {str(e)}")
            return {"error": str(e)}
    
    def is_healthy(self, thresholds: Dict[str, float] = None) -> bool:
        """Check if system is healthy.
        
        Args:
            thresholds: Custom thresholds
        
        Returns:
            Health status
        """
        if thresholds is None:
            thresholds = {
                "cpu_percent": 90,
                "memory_percent": 85,
                "disk_percent": 90
            }
        
        status = self.get_system_status()
        
        if "error" in status:
            return False
        
        system = status["system"]
        
        for key, threshold in thresholds.items():
            if key in system and system[key] > threshold:
                logger.warning(f"System {key} exceeds threshold: {system[key]:.1f}% > {threshold}%")
                return False
        
        return True
    
    def get_performance_metrics(self) -> Dict[str, float]:
        """Get performance metrics.
        
        Returns:
            Performance metrics
        """
        status = self.get_system_status()
        
        if "error" in status:
            return {}
        
        return {
            "uptime_hours": status["uptime_seconds"] / 3600,
            "cpu_usage_percent": status["process"]["cpu_percent"],
            "memory_usage_mb": status["process"]["memory_mb"],
            "system_cpu_percent": status["system"]["cpu_percent"],
            "system_memory_percent": status["system"]["memory_percent"]
        }


class HealthChecker:
    """Checks application health and dependencies."""
    
    def __init__(self):
        self.checks: Dict[str, callable] = {}
        self.monitor = SystemMonitor()
    
    def register_check(self, name: str, check_fn: callable) -> None:
        """Register a health check.
        
        Args:
            name: Check name
            check_fn: Check function
        """
        self.checks[name] = check_fn
    
    def run_checks(self) -> Dict[str, Any]:
        """Run all health checks.
        
        Returns:
            Check results
        """
        results = {
            "timestamp": datetime.utcnow().isoformat(),
            "checks": {},
            "overall_status": "healthy"
        }
        
        # System health
        results["checks"]["system"] = {
            "status": "healthy" if self.monitor.is_healthy() else "unhealthy",
            "details": self.monitor.get_system_status()
        }
        
        # Custom checks
        for name, check_fn in self.checks.items():
            try:
                check_result = check_fn()
                results["checks"][name] = {
                    "status": "healthy" if check_result else "unhealthy",
                    "message": "Check passed" if check_result else "Check failed"
                }
            except Exception as e:
                results["checks"][name] = {
                    "status": "unhealthy",
                    "message": str(e)
                }
        
        # Overall status
        for check in results["checks"].values():
            if check["status"] == "unhealthy":
                results["overall_status"] = "unhealthy"
                break
        
        return results
