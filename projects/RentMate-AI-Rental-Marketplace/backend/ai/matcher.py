from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class ItemMatcher:
    def __init__(self):
        # Load a small, fast pre-trained model
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.item_embeddings = {}

    def update_item_embeddings(self, items):
        """Pre-compute embeddings for all items"""
        for item in items:
            # Combine name, category, and description for rich semantic meaning
            text = f"{item.name} {item.category} {item.description}"
            self.item_embeddings[item.id] = self.model.encode([text])[0]

    def add_single_item(self, item):
        text = f"{item.name} {item.category} {item.description}"
        self.item_embeddings[item.id] = self.model.encode([text])[0]

    def find_matches(self, query, active_items):
        if not query.strip():
            return []

        query_embedding = self.model.encode([query])[0]
        results = []

        for item in active_items:
            if item.id not in self.item_embeddings:
                self.add_single_item(item)
                
            item_emb = self.item_embeddings[item.id]
            
            # Calculate cosine similarity
            # shape needs to be 2D for sklearn
            sim = cosine_similarity([query_embedding], [item_emb])[0][0]
            
            # Convert to percentage
            match_score = int(sim * 100)
            
            # Only consider reasonable matches
            if match_score > 25:
                # Basic matching logic (could be expanded with category/price weights)
                reasons = []
                if match_score > 60:
                    reasons.append("Description is highly semantically similar")
                elif match_score > 40:
                    reasons.append("Possible alternative based on your request")
                
                results.append({
                    "item": item,
                    "match_score": match_score,
                    "reasons": reasons
                })
        
        # Sort by highest match score
        results.sort(key=lambda x: x['match_score'], reverse=True)
        return results

# Singleton instance
matcher = ItemMatcher()
