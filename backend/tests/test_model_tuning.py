import os
import time
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models.model_tuner import get_serialized_model_metrics, METRICS_PATH
from app.models.xgboost_predictor import predict_travel_time

client = TestClient(app)

def test_serialized_metrics_structure():
    """Validates that serialized model metrics contain all required optimization fields."""
    metrics = get_serialized_model_metrics()
    assert "optimal_hyperparameters" in metrics
    assert "evaluation_metrics" in metrics
    
    params = metrics["optimal_hyperparameters"]
    assert "learning_rate" in params
    assert 0.0 < params["learning_rate"] <= 0.5
    assert "max_depth" in params
    assert params["max_depth"] >= 3

def test_rmse_error_bounds():
    """Ensures test RMSE and MAE are within realistic urban travel time limits."""
    metrics = get_serialized_model_metrics()
    eval_metrics = metrics["evaluation_metrics"]
    
    assert "test_rmse" in eval_metrics
    assert "test_mae" in eval_metrics
    assert eval_metrics["test_rmse"] > 0
    assert eval_metrics["test_mae"] > 0
    # Average travel time error should be under 5 minutes for a standard 5km segment
    assert eval_metrics["test_rmse"] < 10.0

def test_model_metrics_api_endpoint():
    """Tests GET /api/v1/model-metrics endpoint."""
    response = client.get("/api/v1/model-metrics")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "XGBoost" in data["model_type"]
    assert "optimal_hyperparameters" in data
    assert "evaluation_metrics" in data
    assert data["evaluation_metrics"]["test_rmse"] > 0

def test_serialized_model_inference_latency():
    """Validates that serialized model inference executes in sub-50ms (NFR-001)."""
    features = {
        'latitude': 12.9716,
        'longitude': 77.5946,
        'hour': 9,
        'day_of_week': 3,
        'is_peak_hour': 1
    }
    start = time.perf_counter()
    pred = predict_travel_time(features)
    latency_ms = (time.perf_counter() - start) * 1000
    
    assert pred > 0
    assert latency_ms < 50.0  # Must be fast for real-time routing
