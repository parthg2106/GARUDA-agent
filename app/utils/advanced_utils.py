"""Advanced utilities for GARUDA."""

import torch
import numpy as np
from typing import Dict, Any, List, Tuple, Optional
from pathlib import Path
import json
from datetime import datetime

from app.config import settings
from app.utils.logger import logger


class ModelCheckpointManager:
    """Manages model checkpoints and versioning."""
    
    def __init__(self, checkpoint_dir: str = settings.CHECKPOINT_DIR):
        self.checkpoint_dir = Path(checkpoint_dir)
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)
        self.metadata: Dict[str, Dict[str, Any]] = {}
    
    def save_checkpoint(
        self,
        model: torch.nn.Module,
        model_name: str,
        epoch: int,
        metrics: Dict[str, float],
        optimizer_state: Optional[Dict[str, Any]] = None
    ) -> str:
        """Save model checkpoint with metadata.
        
        Args:
            model: Model to save
            model_name: Name of model
            epoch: Training epoch
            metrics: Training metrics
            optimizer_state: Optional optimizer state
        
        Returns:
            Checkpoint path
        """
        checkpoint = {
            "epoch": epoch,
            "model_state": model.state_dict(),
            "metrics": metrics,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        if optimizer_state:
            checkpoint["optimizer_state"] = optimizer_state
        
        checkpoint_path = self.checkpoint_dir / f"{model_name}_epoch_{epoch}.pt"
        torch.save(checkpoint, checkpoint_path)
        
        # Update metadata
        if model_name not in self.metadata:
            self.metadata[model_name] = {}
        
        self.metadata[model_name][f"epoch_{epoch}"] = {
            "path": str(checkpoint_path),
            "metrics": metrics,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        logger.info(f"Checkpoint saved: {checkpoint_path}")
        return str(checkpoint_path)
    
    def load_checkpoint(self, checkpoint_path: str) -> Dict[str, Any]:
        """Load checkpoint.
        
        Args:
            checkpoint_path: Path to checkpoint
        
        Returns:
            Checkpoint data
        """
        checkpoint = torch.load(checkpoint_path)
        logger.info(f"Checkpoint loaded: {checkpoint_path}")
        return checkpoint
    
    def get_best_checkpoint(self, model_name: str, metric: str = "loss") -> Optional[str]:
        """Get best checkpoint by metric.
        
        Args:
            model_name: Model name
            metric: Metric to compare
        
        Returns:
            Best checkpoint path or None
        """
        if model_name not in self.metadata or not self.metadata[model_name]:
            return None
        
        best_checkpoint = None
        best_value = float('inf') if 'loss' in metric else 0
        
        for ckpt_name, ckpt_data in self.metadata[model_name].items():
            if metric in ckpt_data["metrics"]:
                value = ckpt_data["metrics"][metric]
                
                if 'loss' in metric:
                    if value < best_value:
                        best_value = value
                        best_checkpoint = ckpt_data["path"]
                else:
                    if value > best_value:
                        best_value = value
                        best_checkpoint = ckpt_data["path"]
        
        return best_checkpoint
    
    def export_metadata(self, filepath: str) -> None:
        """Export metadata to JSON.
        
        Args:
            filepath: Export path
        """
        with open(filepath, 'w') as f:
            json.dump(self.metadata, f, indent=2)
        logger.info(f"Metadata exported to {filepath}")


class PerformanceProfiler:
    """Profiles model performance and inference speed."""
    
    def __init__(self):
        self.profiles: Dict[str, Dict[str, Any]] = {}
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    def profile_model(
        self,
        model: torch.nn.Module,
        model_name: str,
        input_shape: Tuple[int, ...],
        num_runs: int = 100
    ) -> Dict[str, float]:
        """Profile model inference performance.
        
        Args:
            model: Model to profile
            model_name: Model name
            input_shape: Input tensor shape
            num_runs: Number of inference runs
        
        Returns:
            Performance metrics
        """
        model.eval()
        model.to(self.device)
        
        # Warmup
        with torch.no_grad():
            dummy_input = torch.randn(input_shape).to(self.device)
            for _ in range(10):
                _ = model(dummy_input)
        
        # Profile
        import time
        
        times = []
        with torch.no_grad():
            for _ in range(num_runs):
                dummy_input = torch.randn(input_shape).to(self.device)
                
                if self.device.type == 'cuda':
                    torch.cuda.synchronize()
                
                start = time.time()
                _ = model(dummy_input)
                
                if self.device.type == 'cuda':
                    torch.cuda.synchronize()
                
                elapsed = time.time() - start
                times.append(elapsed * 1000)  # Convert to ms
        
        times = np.array(times)
        
        profile = {
            "model_name": model_name,
            "device": str(self.device),
            "input_shape": str(input_shape),
            "mean_latency_ms": float(times.mean()),
            "std_latency_ms": float(times.std()),
            "min_latency_ms": float(times.min()),
            "max_latency_ms": float(times.max()),
            "throughput_samples_per_sec": float(1000 / times.mean()),
            "num_runs": num_runs
        }
        
        self.profiles[model_name] = profile
        logger.info(f"Model {model_name} profiled: {profile['mean_latency_ms']:.2f}ms avg latency")
        
        return profile
    
    def get_model_size(self, model: torch.nn.Module) -> Dict[str, float]:
        """Get model size statistics.
        
        Args:
            model: Model
        
        Returns:
            Size statistics
        """
        total_params = sum(p.numel() for p in model.parameters())
        trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
        
        # Estimate model size in MB
        model_size_mb = (total_params * 4) / (1024 * 1024)  # Assuming float32
        
        return {
            "total_parameters": int(total_params),
            "trainable_parameters": int(trainable_params),
            "estimated_size_mb": float(model_size_mb)
        }
    
    def export_profiles(self, filepath: str) -> None:
        """Export profiles to JSON.
        
        Args:
            filepath: Export path
        """
        with open(filepath, 'w') as f:
            json.dump(self.profiles, f, indent=2)
        logger.info(f"Profiles exported to {filepath}")


class HyperparameterTuner:
    """Utilities for hyperparameter tuning."""
    
    @staticmethod
    def grid_search(
        param_grid: Dict[str, List[Any]],
        train_fn,
        num_trials: int = 10
    ) -> List[Dict[str, Any]]:
        """Grid search over hyperparameters.
        
        Args:
            param_grid: Parameter grid
            train_fn: Training function
            num_trials: Number of trials
        
        Returns:
            Results list
        """
        import itertools
        
        results = []
        param_combinations = list(itertools.product(*param_grid.values()))
        
        for trial_idx, params in enumerate(param_combinations[:num_trials]):
            param_dict = {key: val for key, val in zip(param_grid.keys(), params)}
            logger.info(f"Trial {trial_idx + 1}/{min(num_trials, len(param_combinations))}: {param_dict}")
            
            result = train_fn(**param_dict)
            result["params"] = param_dict
            results.append(result)
        
        return results
    
    @staticmethod
    def random_search(
        param_distributions: Dict[str, Any],
        train_fn,
        num_trials: int = 10,
        random_state: int = 42
    ) -> List[Dict[str, Any]]:
        """Random search over hyperparameters.
        
        Args:
            param_distributions: Parameter distributions
            train_fn: Training function
            num_trials: Number of trials
            random_state: Random seed
        
        Returns:
            Results list
        """
        np.random.seed(random_state)
        results = []
        
        for trial_idx in range(num_trials):
            param_dict = {}
            for key, dist in param_distributions.items():
                if isinstance(dist, list):
                    param_dict[key] = np.random.choice(dist)
                else:
                    param_dict[key] = dist()
            
            logger.info(f"Trial {trial_idx + 1}/{num_trials}: {param_dict}")
            result = train_fn(**param_dict)
            result["params"] = param_dict
            results.append(result)
        
        return results


class ModelExporter:
    """Exports models to different formats."""
    
    @staticmethod
    def export_to_onnx(
        model: torch.nn.Module,
        input_shape: Tuple[int, ...],
        output_path: str
    ) -> None:
        """Export model to ONNX format.
        
        Args:
            model: PyTorch model
            input_shape: Input tensor shape
            output_path: Output path
        """
        try:
            import onnx
            
            dummy_input = torch.randn(input_shape)
            torch.onnx.export(
                model,
                dummy_input,
                output_path,
                verbose=False,
                input_names=['input'],
                output_names=['output']
            )
            logger.info(f"Model exported to ONNX: {output_path}")
        except ImportError:
            logger.error("ONNX export requires onnx package")
    
    @staticmethod
    def export_to_torchscript(
        model: torch.nn.Module,
        output_path: str
    ) -> None:
        """Export model to TorchScript format.
        
        Args:
            model: PyTorch model
            output_path: Output path
        """
        scripted_model = torch.jit.script(model)
        torch.jit.save(scripted_model, output_path)
        logger.info(f"Model exported to TorchScript: {output_path}")
