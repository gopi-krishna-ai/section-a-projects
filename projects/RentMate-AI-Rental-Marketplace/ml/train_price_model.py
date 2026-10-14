import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import pickle
import os

def train_model():
    print("Generating synthetic training data for rental prices...")
    # Generate some realistic training data based on Categories and Conditions
    np.random.seed(42)
    
    categories = ['Furniture', 'Electronics', 'Home Appliances', 'Kitchen', 'Tools', 'Outdoor', 'Moving', 'Events', 'Transport']
    conditions = ['Excellent', 'Good', 'Fair']
    
    # Base prices for categories
    base_prices = {
        'Furniture': 100, 'Electronics': 400, 'Home Appliances': 150, 
        'Kitchen': 120, 'Tools': 180, 'Outdoor': 250, 
        'Moving': 150, 'Events': 200, 'Transport': 300
    }
    
    # Condition multipliers
    cond_multipliers = {'Excellent': 1.2, 'Good': 1.0, 'Fair': 0.7}
    
    data = []
    for _ in range(5000): # 5000 samples for better accuracy
        cat = np.random.choice(categories)
        cond = np.random.choice(conditions)
        
        # Calculate base price with some random noise
        price = base_prices[cat] * cond_multipliers[cond]
        noise = np.random.normal(0, price * 0.05) # Reduced noise to 5% for better fit
        final_price = max(10, int(price + noise))
        
        data.append({'category': cat, 'condition': cond, 'price': final_price})
        
    df = pd.DataFrame(data)
    
    print("Preprocessing data (Label Encoding)...")
    le_cat = LabelEncoder()
    le_cond = LabelEncoder()
    
    df['category_encoded'] = le_cat.fit_transform(df['category'])
    df['condition_encoded'] = le_cond.fit_transform(df['condition'])
    
    X = df[['category_encoded', 'condition_encoded']]
    y = df['price']
    
    print("Training Random Forest Regressor model...")
    # Increase estimators for better accuracy
    model = RandomForestRegressor(n_estimators=300, max_depth=10, random_state=42)
    model.fit(X, y)
    
    print("Model trained successfully. Accuracy (R^2 Score):", model.score(X, y))
    
    # Save the model and encoders
    os.makedirs('saved_models', exist_ok=True)
    with open('saved_models/price_model.pkl', 'wb') as f:
        pickle.dump({
            'model': model,
            'cat_encoder': le_cat,
            'cond_encoder': le_cond
        }, f)
        
    print("Model and encoders saved to ml/saved_models/price_model.pkl")

if __name__ == "__main__":
    train_model()
