import os
import pickle
import numpy as np

class PriceAssistant:
    def __init__(self):
        self.model_data = None
        self.load_model()
        
    def load_model(self):
        # Path to the trained model in the ml/ directory
        base_dir = os.path.abspath(os.path.dirname(__file__))
        model_path = os.path.join(base_dir, '..', '..', 'ml', 'saved_models', 'price_model.pkl')
        
        if os.path.exists(model_path):
            try:
                with open(model_path, 'rb') as f:
                    self.model_data = pickle.load(f)
                print("Successfully loaded Random Forest price prediction model.")
            except Exception as e:
                print(f"Error loading model: {e}")
        else:
            print(f"Model not found at {model_path}. Using fallback rules.")
            
    def suggest_price(self, category, name, condition='Good'):
        if self.model_data:
            try:
                # Use the trained Random Forest model
                model = self.model_data['model']
                cat_encoder = self.model_data['cat_encoder']
                cond_encoder = self.model_data['cond_encoder']
                
                # Handle unknown categories gracefully
                if category not in cat_encoder.classes_:
                    category = 'Other' if 'Other' in cat_encoder.classes_ else cat_encoder.classes_[0]
                if condition not in cond_encoder.classes_:
                    condition = 'Good'
                
                cat_encoded = cat_encoder.transform([category])[0]
                cond_encoded = cond_encoder.transform([condition])[0]
                
                # Predict
                X = np.array([[cat_encoded, cond_encoded]])
                predicted_price = model.predict(X)[0]
                
                price = int(predicted_price)
                return {
                    "suggested_price": price,
                    "range_min": int(price * 0.85),
                    "range_max": int(price * 1.15),
                    "message": "AI prediction using Random Forest Regressor."
                }
            except Exception as e:
                print(f"Prediction error: {e}")
                
        # Fallback if model not loaded or fails
        defaults = {
            'Furniture': 100, 'Electronics': 400, 'Home Appliances': 150,
            'Kitchen': 150, 'Tools': 150, 'Outdoor': 200, 'Moving': 100,
            'Events': 100, 'Transport': 200
        }
        avg = defaults.get(category, 100)
        return {
            "suggested_price": avg,
            "range_min": int(avg * 0.8),
            "range_max": int(avg * 1.2),
            "message": "Fallback rule-based suggestion."
        }

price_assistant = PriceAssistant()
