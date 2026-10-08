import xgboost as xgb
import pandas as pd
import os
import pickle

MODEL_PATH = "data/processed/xgb_baseline.pkl"

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
    """Loads the model and predicts travel time."""
    if not os.path.exists(MODEL_PATH):
        return 25.0 # Fallback dummy value if model not trained yet
        
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
        
    df = pd.DataFrame([features_dict])
    return float(model.predict(df)[0])

if __name__ == "__main__":
    train_baseline_xgboost("data/processed/cleaned_traffic_features.csv")
