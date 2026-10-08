import pandas as pd
import numpy as np
import os

# Hardcoded approximate coordinates for Kaggle dataset areas to satisfy OSRM routing ML features
AREA_COORDS = {
    'Indiranagar': (12.9784, 77.6408),
    'Whitefield': (12.9698, 77.7499),
    'Koramangala': (12.9279, 77.6271),
    'Electronic City': (12.8452, 77.6602),
    'Jayanagar': (12.9299, 77.5826),
    'Marathahalli': (12.9569, 77.7011),
    'Bellandur': (12.9304, 77.6784),
    'HSR Layout': (12.9121, 77.6446),
    'BTM Layout': (12.9166, 77.6101),
    'Malleswaram': (13.0031, 77.5643)
}

def preprocess_traffic_data(raw_csv_path: str, processed_csv_path: str) -> pd.DataFrame:
    print(f"Loading raw dataset from {raw_csv_path}...")
    try:
        df = pd.read_csv(raw_csv_path)
    except FileNotFoundError:
        print(f"Error: Could not find dataset at {raw_csv_path}")
        return None

    print(f"Original shape: {df.shape}")
    
    # 1. Adapt Kaggle dataset columns to match README specifications
    if 'Date' in df.columns:
        df.rename(columns={'Date': 'timestamp'}, inplace=True)
    
    # Generate spatial features (latitude, longitude) by mapping the 'Area Name'
    if 'Area Name' in df.columns:
        df['latitude'] = df['Area Name'].map(lambda x: AREA_COORDS.get(x, (np.nan, np.nan))[0])
        df['longitude'] = df['Area Name'].map(lambda x: AREA_COORDS.get(x, (np.nan, np.nan))[1])
        
    # Generate target variable (travel_time) assuming a standardized 5km segment distance
    # travel_time (minutes) = (Distance / Average Speed) * 60
    if 'Average Speed' in df.columns:
        df['travel_time'] = (5.0 / df['Average Speed']) * 60

    # 2. Execute README.md preprocessing logic
    df.dropna(subset=['latitude', 'longitude', 'travel_time'], inplace=True)
    
    # Extract temporal signals
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['hour'] = df['timestamp'].dt.hour
    df['day_of_week'] = df['timestamp'].dt.dayofweek
    
    # Peak hour indicator
    df['is_peak_hour'] = df['hour'].apply(lambda h: 1 if (8 <= h <= 10 or 17 <= h <= 20) else 0)
    
    # Outlier removal via IQR method
    q1 = df['travel_time'].quantile(0.25)
    q3 = df['travel_time'].quantile(0.75)
    iqr = q3 - q1
    df = df[(df['travel_time'] >= q1 - 1.5 * iqr) & (df['travel_time'] <= q3 + 1.5 * iqr)]
    
    print(f"Cleaned shape after dropping nulls and outliers: {df.shape}")
    
    df.to_csv(processed_csv_path, index=False)
    print(f"Successfully saved processed data to {processed_csv_path}")
    
    return df

if __name__ == "__main__":
    os.makedirs("data/processed", exist_ok=True)
    RAW_PATH = "data/raw/bangalore_traffic_pulse.csv"
    PROCESSED_PATH = "data/processed/cleaned_traffic_features.csv"
    preprocess_traffic_data(RAW_PATH, PROCESSED_PATH)
