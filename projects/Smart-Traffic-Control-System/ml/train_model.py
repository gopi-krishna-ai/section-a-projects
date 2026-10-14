import pandas as pd
import numpy as np
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

def generate_data(num_samples=1000):
    np.random.seed(42)
    # Features: hour (0-23), day_of_week (0-6), weather (0=Clear, 1=Rain, 2=Fog), vehicle_count (0-100)
    hour = np.random.randint(0, 24, num_samples)
    day_of_week = np.random.randint(0, 7, num_samples)
    weather = np.random.randint(0, 3, num_samples)
    vehicle_count = np.random.randint(2, 60, num_samples)
    
    # Target: optimal_green_time (seconds)
    optimal_green_time = 20.0 + (vehicle_count * 0.5)
    optimal_green_time += np.where(np.isin(hour, [8,9,17,18]), 15.0, 0.0) # Rush hour boost
    optimal_green_time += (weather * 5.0) # Rain/Fog adds time to clear intersection
    # Add some noise
    optimal_green_time += np.random.normal(0, 2, num_samples)
    
    df = pd.DataFrame({
        'hour': hour,
        'day_of_week': day_of_week,
        'weather': weather,
        'vehicle_count': vehicle_count,
        'optimal_green_time': optimal_green_time
    })
    return df

def train():
    print("Generating synthetic traffic dataset...")
    df = generate_data()
    df.to_csv('ml/traffic_data.csv', index=False)
    
    X = df.drop('optimal_green_time', axis=1)
    y = df['optimal_green_time']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Training Random Forest Regressor...")
    model = RandomForestRegressor(n_estimators=50, random_state=42)
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    print(f"Model R2 Score: {r2_score(y_test, y_pred):.4f}")
    print(f"Model MSE: {mean_squared_error(y_test, y_pred):.4f}")
    
    os.makedirs('ml/models', exist_ok=True)
    joblib.dump(model, 'ml/models/green_time_model.pkl')
    print("Model saved to ml/models/green_time_model.pkl")

if __name__ == '__main__':
    train()
