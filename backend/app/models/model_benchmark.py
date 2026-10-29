import os
import json
import time
import numpy as np
import pandas as pd
import xgboost as xgb
from datetime import datetime
from pathlib import Path
from typing import Dict, Any
from sklearn.model_selection import KFold
from sklearn.dummy import DummyRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

from app.core.config import settings
from app.models.model_registry import register_serialized_model

BENCHMARK_PATH = settings.BASE_DIR / "data" / "processed" / "benchmark_results.json"

def run_cross_validation_benchmark(
    csv_path: str = None,
    n_splits: int = 5
) -> Dict[str, Any]:
    """
    Executes 5-Fold Cross Validation benchmarking travel time models:
    1. Dummy Regressor (Mean baseline)
    2. Decision Tree Regressor
    3. Tuned XGBoost Regressor (with optimal learning rate)
    
    Profiles sub-200ms inference latency (NFR-001) and serializes results.
    """
    data_file = csv_path or str(settings.PROCESSED_DATA_PATH)
    if not os.path.exists(data_file):
        raise FileNotFoundError(f"Processed dataset not found at {data_file}")
        
    df = pd.read_csv(data_file)
    feature_cols = ['latitude', 'longitude', 'hour', 'day_of_week', 'is_peak_hour']
    target_col = 'travel_time'
    
    X = df[feature_cols].values
    y = df[target_col].values
    
    kf = KFold(n_splits=n_splits, shuffle=True, random_state=42)
    
    results = {
        "Dummy (Mean Baseline)": {"rmse": [], "mae": []},
        "Decision Tree": {"rmse": [], "mae": [], "r2": []},
        "Tuned XGBoost Regressor": {"rmse": [], "mae": [], "r2": []}
    }
    
    for train_idx, test_idx in kf.split(X):
        X_train, X_test = X[train_idx], X[test_idx]
        y_train, y_test = y[train_idx], y[test_idx]
        
        # 1. Dummy Baseline
        dummy = DummyRegressor(strategy="mean")
        dummy.fit(X_train, y_train)
        pred_dummy = dummy.predict(X_test)
        results["Dummy (Mean Baseline)"]["rmse"].append(float(np.sqrt(mean_squared_error(y_test, pred_dummy))))
        results["Dummy (Mean Baseline)"]["mae"].append(float(mean_absolute_error(y_test, pred_dummy)))
        
        # 2. Decision Tree
        dt = DecisionTreeRegressor(max_depth=6, random_state=42)
        dt.fit(X_train, y_train)
        pred_dt = dt.predict(X_test)
        results["Decision Tree"]["rmse"].append(float(np.sqrt(mean_squared_error(y_test, pred_dt))))
        results["Decision Tree"]["mae"].append(float(mean_absolute_error(y_test, pred_dt)))
        results["Decision Tree"]["r2"].append(float(r2_score(y_test, pred_dt)))
        
        # 3. Tuned XGBoost
        model_xgb = xgb.XGBRegressor(
            n_estimators=120,
            learning_rate=0.01,
            max_depth=5,
            subsample=0.85,
            colsample_bytree=0.85,
            random_state=42,
            n_jobs=-1
        )
        model_xgb.fit(X_train, y_train)
        pred_xgb = model_xgb.predict(X_test)
        results["Tuned XGBoost Regressor"]["rmse"].append(float(np.sqrt(mean_squared_error(y_test, pred_xgb))))
        results["Tuned XGBoost Regressor"]["mae"].append(float(mean_absolute_error(y_test, pred_xgb)))
        results["Tuned XGBoost Regressor"]["r2"].append(float(r2_score(y_test, pred_xgb)))

    # Compute aggregate metrics
    aggregated = {}
    for model_name, metrics in results.items():
        aggregated[model_name] = {
            "mean_rmse": round(float(np.mean(metrics["rmse"])), 4),
            "std_rmse": round(float(np.std(metrics["rmse"])), 4),
            "mean_mae": round(float(np.mean(metrics["mae"])), 4),
            "std_mae": round(float(np.std(metrics["mae"])), 4),
            "mean_r2": round(float(np.mean(metrics.get("r2", [0.0]))), 4)
        }
        
    # Latency Profiling (100 synthetic routing inference queries per NFR-001)
    sample_rows = X[:100]
    latencies = []
    
    # Warmup
    model_xgb.predict(sample_rows[:2])
    
    for row in sample_rows:
        t0 = time.perf_counter()
        model_xgb.predict(row.reshape(1, -1))
        latencies.append((time.perf_counter() - t0) * 1000.0) # ms
        
    latency_stats = {
        "mean_latency_ms": round(float(np.mean(latencies)), 2),
        "p50_latency_ms": round(float(np.percentile(latencies, 50)), 2),
        "p95_latency_ms": round(float(np.percentile(latencies, 95)), 2),
        "p99_latency_ms": round(float(np.percentile(latencies, 99)), 2),
        "max_latency_ms": round(float(np.max(latencies)), 2),
        "meets_nfr001_sub_200ms": bool(np.percentile(latencies, 99) < 200.0)
    }

    # Register model
    registry_meta = register_serialized_model()

    payload = {
        "benchmark_title": "5-Fold Cross-Validation Model Comparison",
        "dataset_rows": len(df),
        "n_splits": n_splits,
        "models_evaluated": aggregated,
        "latency_profile": latency_stats,
        "active_model_registry": registry_meta,
        "timestamp": datetime.now().isoformat()
    }
    
    os.makedirs(BENCHMARK_PATH.parent, exist_ok=True)
    with open(BENCHMARK_PATH, "w") as f:
        json.dump(payload, f, indent=2)
        
    return payload

def get_benchmark_results() -> Dict[str, Any]:
    """Loads existing benchmark results or computes them on-demand."""
    if BENCHMARK_PATH.exists():
        try:
            with open(BENCHMARK_PATH, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return run_cross_validation_benchmark()

if __name__ == "__main__":
    run_cross_validation_benchmark()
