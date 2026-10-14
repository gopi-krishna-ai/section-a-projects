import os
import pickle
from backend.models import db, Category, Product, Interaction

class RecommendationEngine:
    def __init__(self):
        self.model = None
        self._load_model()
        
    def _load_model(self):
        model_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'ml', 'saved_model.pkl')
        if os.path.exists(model_path):
            with open(model_path, 'rb') as f:
                self.model = pickle.load(f)
                
    def generate_features_for_customer(self, customer_id):
        categories = Category.query.all()
        interactions = Interaction.query.filter_by(customer_id=customer_id).all()
        
        cat_interactions = {c.id: [] for c in categories}
        for i in interactions:
            if i.category_id in cat_interactions:
                cat_interactions[i.category_id].append(i)
                
        features_list = []
        for cat in categories:
            group = cat_interactions[cat.id]
            views = sum(1 for x in group if x.interaction_type == 'VIEW')
            adds = sum(1 for x in group if x.interaction_type == 'ADD_TO_CART')
            wishlists = sum(1 for x in group if x.interaction_type == 'WISHLIST')
            searches = sum(1 for x in group if x.interaction_type == 'SEARCH')
            purchases = sum(1 for x in group if x.interaction_type == 'PURCHASE')
            
            features_list.append({
                'category_id': cat.id,
                'category_name': cat.name,
                'features': [views, adds, wishlists, searches],
                'views': views,
                'adds': adds,
                'purchases': purchases
            })
            
        return features_list

    def get_recommendations(self, customer_id, limit=8):
        if not self.model:
            return [], []
            
        features = self.generate_features_for_customer(customer_id)
        if not features:
            return [], []
            
        X = [f['features'] for f in features]
        probs = self.model.predict_proba(X)
        
        # Add probability to features
        for i, f in enumerate(features):
            f['probability'] = probs[i][1] # Probability of class 1
            
        # Sort by probability descending
        features.sort(key=lambda x: x['probability'], reverse=True)
        
        recommended_products = []
        explanations = {}
        
        for f in features:
            if len(recommended_products) >= limit:
                break
                
            prods = Product.query.filter_by(category_id=f['category_id']).limit(4).all()
            for p in prods:
                if len(recommended_products) >= limit:
                    break
                if p not in recommended_products:
                    recommended_products.append(p)
                    
                    if f['purchases'] > 0:
                        explanations[p.id] = f"Recommended because you frequently purchase products from the {f['category_name']} category."
                    elif f['views'] > 5:
                        explanations[p.id] = f"You recently viewed products similar to this one in {f['category_name']}."
                    elif f['adds'] > 0:
                        explanations[p.id] = f"You have shown interest by adding {f['category_name']} items to your cart before."
                    else:
                        explanations[p.id] = f"Based on your shopping history, you may want to check this {f['category_name']} product."
                        
        return recommended_products, explanations
