import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    PROJECT_NAME: str = "Smart Sustainable Transport Optimization API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Environment & Host
    PORT: int = 8000
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # External APIs & DB
    OPENWEATHER_API_KEY: str = "dummy_key_for_now"
    MONGODB_URI: str = "mongodb://localhost:27017/smart_transport"
    
    # Base directory paths
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    MODEL_PATH: Path = BASE_DIR / "data" / "processed" / "xgb_baseline.pkl"
    PROCESSED_DATA_PATH: Path = BASE_DIR / "data" / "processed" / "cleaned_traffic_features.csv"

settings = Settings()

