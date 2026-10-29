import os
import hashlib
import json
import pickle
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
from app.core.config import settings

REGISTRY_PATH = settings.BASE_DIR / "data" / "processed" / "model_registry.json"

def calculate_file_hash(file_path: Path | str) -> str:
    """Computes SHA-256 checksum of serialized model artifact for integrity verification."""
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(8192):
            sha256.update(chunk)
    return sha256.hexdigest()

def register_serialized_model(
    model_version: str = "1.1.0-tuned",
    description: str = "Hyperparameter-tuned XGBoost travel time regressor with minimized RMSE"
) -> Dict[str, Any]:
    """
    Registers and verifies the serialized model artifact in the project registry.
    Ensures model artifact integrity, versioning, and reproducibility.
    """
    model_path = Path(settings.MODEL_PATH)
    if not model_path.exists():
        raise FileNotFoundError(f"Model artifact not found at {model_path}")
        
    file_size_bytes = model_path.stat().st_size
    file_hash = calculate_file_hash(model_path)
    
    # Verify unpickling integrity
    with open(model_path, "rb") as f:
        loaded_model = pickle.load(f)
    n_features = getattr(loaded_model, "n_features_in_", 5)
    
    registry_data = {
        "model_version": model_version,
        "artifact_file": model_path.name,
        "sha256_checksum": file_hash,
        "size_bytes": file_size_bytes,
        "n_features_expected": int(n_features),
        "status": "active_production",
        "description": description,
        "registered_at": datetime.now().isoformat()
    }
    
    os.makedirs(REGISTRY_PATH.parent, exist_ok=True)
    with open(REGISTRY_PATH, "w") as f:
        json.dump(registry_data, f, indent=2)
        
    return registry_data

def get_model_registry_info() -> Dict[str, Any]:
    """Retrieves current model registry metadata."""
    if REGISTRY_PATH.exists():
        try:
            with open(REGISTRY_PATH, "r") as f:
                return json.load(f)
        except Exception:
            pass
            
    # Auto-register if not yet created
    if Path(settings.MODEL_PATH).exists():
        return register_serialized_model()
        
    return {
        "model_version": "1.0.0-baseline",
        "status": "unverified",
        "registered_at": datetime.now().isoformat()
    }
