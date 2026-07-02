"""Metrics collection and tracking."""

from typing import Dict, List, Any
from datetime import datetime
from collections import defaultdict
import json
from pathlib import Path
from app.config import settings


class MetricsCollector:
    """Collects and tracks system metrics."""
    
    def __init__(self):
        self.metrics: Dict[str, List[float]] = defaultdict(list)
        self.counters: Dict[str, int] = defaultdict(int)
        self.timestamps: Dict[str, List[datetime]] = defaultdict(list)
    
    def record_metric(self, name: str, value: float, timestamp: Optional[datetime] = None) -> None:
        """Record a metric value.
        
        Args:
            name: Metric name
            value: Metric value
            timestamp: Optional timestamp
        """
        self.metrics[name].append(value)
        self.timestamps[name].append(timestamp or datetime.utcnow())
    
    def increment_counter(self, name: str, amount: int = 1) -> None:
        """Increment a counter.
        
        Args:
            name: Counter name
            amount: Amount to increment
        """
        self.counters[name] += amount
    
    def get_metric_stats(self, name: str) -> Dict[str, float]:
        """Get statistics for a metric.
        
        Args:
            name: Metric name
        
        Returns:
            Dictionary with min, max, mean, count
        """
        if name not in self.metrics or len(self.metrics[name]) == 0:
            return {"min": 0, "max": 0, "mean": 0, "count": 0}
        
        values = self.metrics[name]
        return {
            "min": min(values),
            "max": max(values),
            "mean": sum(values) / len(values),
            "count": len(values)
        }
    
    def get_counter(self, name: str) -> int:
        """Get counter value.
        
        Args:
            name: Counter name
        
        Returns:
            Counter value
        """
        return self.counters.get(name, 0)
    
    def reset(self) -> None:
        """Reset all metrics."""
        self.metrics.clear()
        self.counters.clear()
        self.timestamps.clear()
    
    def export_metrics(self, filepath: Optional[str] = None) -> Dict[str, Any]:
        """Export metrics to dictionary or file.
        
        Args:
            filepath: Optional file path to save metrics
        
        Returns:
            Metrics dictionary
        """
        export_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "metrics": {name: self.get_metric_stats(name) for name in self.metrics},
            "counters": dict(self.counters)
        }
        
        if filepath:
            output_path = Path(settings.TRAINING_OUTPUT_DIR) / filepath
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w') as f:
                json.dump(export_data, f, indent=2)
        
        return export_data


from typing import Optional
