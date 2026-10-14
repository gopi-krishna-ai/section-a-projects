import os
os.environ["DISABLE_SQLALCHEMY_CEXT"] = "1"
import sys
import pickle
import random
from datetime import datetime
from ml.pure_rf import PureRandomForestClassifier

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import app
from backend.models import db, Customer, Category, Product, Interaction

def train_recommendation_model():
    print("Extracting data for training...")
    with app.app_context():
        interactions = Interaction.query.all()
        
        # Group by customer and category
        grouped = {}
        for i in interactions:
            key = (i.customer_id, i.category_id)
            if key not in grouped:
                grouped[key] = []
            grouped[key].append(i)
            
        if not grouped:
            print("No interactions found. Cannot train model.")
            return

        print("Engineering features...")
        features_list = []
        for (cust_id, cat_id), group in grouped.items():
            views = sum(1 for x in group if x.interaction_type == 'VIEW')
            adds = sum(1 for x in group if x.interaction_type == 'ADD_TO_CART')
            wishlists = sum(1 for x in group if x.interaction_type == 'WISHLIST')
            searches = sum(1 for x in group if x.interaction_type == 'SEARCH')
            purchases = sum(1 for x in group if x.interaction_type == 'PURCHASE')
            
            target = 1 if purchases > 0 else 0
            features_list.append([views, adds, wishlists, searches, target])
            
        # Ensure we have both classes
        targets = [f[4] for f in features_list]
        if 0 not in targets:
            features_list.append([0, 0, 0, 0, 0])
        if 1 not in targets:
            features_list.append([10, 5, 2, 1, 1])
            
        # Shuffle
        random.seed(42)
        random.shuffle(features_list)
        
        split_idx = int(len(features_list) * 0.8)
        train_data = features_list[:split_idx]
        test_data = features_list[split_idx:]
        
        X_train = [row[:4] for row in train_data]
        y_train = [row[4] for row in train_data]
        X_test = [row[:4] for row in test_data]
        y_test = [row[4] for row in test_data]
        
        print("Training Pure Python Random Forest Classifier...")
        rf = PureRandomForestClassifier(n_estimators=10, max_depth=5)
        rf.fit(X_train, y_train)
        
        # Evaluate manually
        y_pred = rf.predict(X_test)
        correct = sum(1 for i in range(len(y_test)) if y_test[i] == y_pred[i])
        accuracy = correct / len(y_test) if y_test else 0.0
        
        print("\n--- Model Evaluation ---")
        print(f"Accuracy: {accuracy:.4f}")
        
        # Save model
        model_path = os.path.join(os.path.dirname(__file__), 'saved_model.pkl')
        with open(model_path, 'wb') as f:
            pickle.dump(rf, f)
        print(f"Model saved to {model_path}")

if __name__ == '__main__':
    train_recommendation_model()
