import sys
sys.path.append(r'C:\Users\krish\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.12_qbz5n2kfra8p0\LocalCache\local-packages\Python312\site-packages')

import os
# Force transformers to run in offline mode so it doesn't try to connect to HF Hub
os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["TRANSFORMERS_OFFLINE"] = "1"

try:
    from sentence_transformers import SentenceTransformer, util
    # Load from local cache directly
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    
    # We embed a set of 'disaster' definitions
    DISASTER_PROMPTS = [
        "A critical emergency, disaster, or terrorist attack requiring immediate rescue and police or medical attention.",
        "A devastating natural disaster such as a flood, earthquake, or wildfire.",
        "A major transport accident or building collapse with casualties."
    ]
    SAFE_PROMPTS = [
        "A normal everyday event, random conversation, or news about a movie.",
        "A casual observation about the weather or a metaphor.",
        "A joke or non-urgent political statement."
    ]
    
    disaster_emb = model.encode(DISASTER_PROMPTS, convert_to_tensor=True)
    safe_emb = model.encode(SAFE_PROMPTS, convert_to_tensor=True)
    
    def get_pretrained_confidence(text):
        if not text:
            return 0.0
        text_emb = model.encode(text, convert_to_tensor=True)
        # Compute cosine similarities
        disaster_scores = util.cos_sim(text_emb, disaster_emb)[0]
        safe_scores = util.cos_sim(text_emb, safe_emb)[0]
        
        max_disaster = float(disaster_scores.max())
        max_safe = float(safe_scores.max())
        
        # If disaster score is significantly higher, boost confidence
        if max_disaster > max_safe:
            # Normalize to a confidence score 50-99
            diff = max_disaster - max_safe
            return min(0.99, 0.5 + (diff * 2.5))
        else:
            return max(0.0, 0.5 - ((max_safe - max_disaster) * 2.5))

except Exception as e:
    print(f"Warning: Pretrained model could not be loaded ({e})")
    def get_pretrained_confidence(text):
        return None
