import xgboost as xgb
import pandas as pd
import os
import pickle
from pathlib import Path
from app.core.config import settings

MODEL_PATH = str(settings.MODEL_PATH)
if not os.path.exists(MODEL_PATH):
    # Fallback to local directory relative to file
    fallback_path = Path(__file__).resolve().parent.parent.parent / "data" / "processed" / "xgb_baseline.pkl"
    if fallback_path.exists():
        MODEL_PATH = str(fallback_path)

def train_baseline_xgboost(csv_path: str):
    """
    Trains a baseline XGBoost model to predict travel_time 
    using spatial and temporal features.
    """
    print(f"Loading features from {csv_path}...")
    df = pd.read_csv(csv_path)
    
    # Select features (X) and target (y)
    features = ['latitude', 'longitude', 'hour', 'day_of_week', 'is_peak_hour']
    X = df[features]
    y = df['travel_time']
    
    print("Training XGBoost Regressor...")
    model = xgb.XGBRegressor(
        n_estimators=100, 
        learning_rate=0.1, 
        max_depth=5,
        random_state=42
    )
    
    model.fit(X, y)
    
    # Save the model
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)
        
    print(f"Model successfully saved to {MODEL_PATH}")

def predict_travel_time(features_dict: dict) -> float:
    """Loads the model and predicts travel time for standard 5km road segment."""
    if not os.path.exists(MODEL_PATH):
        return 25.0  # Fallback default value if model not trained yet
        
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
        
    df = pd.DataFrame([features_dict])
    return float(model.predict(df)[0])

def predict_weather_adjusted_travel_time(
    features_dict: dict,
    rainfall_mm: float = 0.0,
    distance_km: float = 5.0
) -> dict:
    """
    Predicts weather- and road-based travel times (Form 2 milestone: 04-10-2026 to 18-10-2026).
    Combines spatial/temporal XGBoost regression with live precipitation friction modeling.
    """
    base_5km_time = predict_travel_time(features_dict)
    
    # Scale from 5km standard segment to actual route distance
    safe_dist = max(distance_km, 0.5)
    scaled_road_time = (base_5km_time / 5.0) * safe_dist
    
    # Weather-friction coefficient: precipitation increases road delay and reduces vehicle speed
    weather_multiplier = 1.0 + min(max(rainfall_mm, 0.0) * 0.025, 0.35)
    adjusted_time = round(scaled_road_time * weather_multiplier, 2)
    weather_delay_min = round(adjusted_time - scaled_road_time, 2)
    
    return {
        "base_travel_time_min": round(scaled_road_time, 2),
        "weather_adjusted_travel_time_min": max(adjusted_time, 3.0),
        "weather_delay_min": max(weather_delay_min, 0.0),
        "rainfall_mm": rainfall_mm,
        "distance_km": round(safe_dist, 2)
    }

if __name__ == "__main__":
    train_baseline_xgboost("data/processed/cleaned_traffic_features.csv")
