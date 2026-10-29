import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models.model_benchmark import get_benchmark_results
from app.models.model_registry import get_model_registry_info, calculate_file_hash
from app.core.config import settings

client = TestClient(app)

def test_benchmark_data_structure():
    """Validates structure and presence of required cross-validation benchmarks."""
    benchmark = get_benchmark_results()
    assert "models_evaluated" in benchmark
    assert "latency_profile" in benchmark
    assert "active_model_registry" in benchmark
    
    models = benchmark["models_evaluated"]
    assert "Dummy (Mean Baseline)" in models
    assert "Tuned XGBoost Regressor" in models
    
    # Tuned XGBoost must achieve lower or competitive RMSE
    xgb_rmse = models["Tuned XGBoost Regressor"]["mean_rmse"]
    assert xgb_rmse > 0
    assert xgb_rmse < 5.0

def test_latency_profile_meets_nfr001():
    """Validates that routing inference latency meets NFR-001 sub-200ms threshold."""
    benchmark = get_benchmark_results()
    latency = benchmark["latency_profile"]
    
    assert "mean_latency_ms" in latency
    assert "p99_latency_ms" in latency
    assert latency["meets_nfr001_sub_200ms"] is True
    # In practice inference on CPU should be well under 10ms
    assert latency["p99_latency_ms"] < 50.0

def test_model_registry_integrity():
    """Validates model artifact registration and SHA-256 checksum verification."""
    registry = get_model_registry_info()
    assert "sha256_checksum" in registry
    assert len(registry["sha256_checksum"]) == 64  # Valid SHA-256 hex string
    assert registry["status"] == "active_production"
    
    # Recalculate checksum directly from file
    actual_hash = calculate_file_hash(settings.MODEL_PATH)
    assert actual_hash == registry["sha256_checksum"]

def test_get_model_benchmark_api_endpoint():
    """Tests GET /api/v1/model-benchmark API contract."""
    response = client.get("/api/v1/model-benchmark")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "models_evaluated" in data
    assert "latency_profile" in data
    assert data["latency_profile"]["meets_nfr001_sub_200ms"] is True
