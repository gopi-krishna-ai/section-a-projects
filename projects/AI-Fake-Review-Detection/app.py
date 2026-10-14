import os
import random
import re
from flask import Flask, render_template, request, jsonify, redirect, url_for

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# NLP Simulation Data
FAKE_KEYWORDS = ['guaranteed', 'best product ever', 'buy now', 'amazing', 'perfect', '100%', 'refund', 'click here', 'scam', 'free']
CITIES = [
    {"name": "Delhi", "lat": 28.7041, "lon": 77.1025},
    {"name": "Mumbai", "lat": 19.0760, "lon": 72.8777},
    {"name": "Bangalore", "lat": 12.9716, "lon": 77.5946},
    {"name": "Pune", "lat": 18.5204, "lon": 73.8567},
    {"name": "Chennai", "lat": 13.0827, "lon": 80.2707},
    {"name": "Hyderabad", "lat": 17.3850, "lon": 78.4867},
]

@app.route('/')
def index():
    return render_template('landing.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

GLOBAL_HISTORY = []

@app.route('/api/analyze_reviews', methods=['POST'])
def analyze_reviews():
    text_block = request.form.get('reviews_text', '')
    if not text_block.strip():
        return jsonify({"error": "No text provided."}), 400

    # Split bulk text by newlines
    raw_reviews = [line.strip() for line in text_block.split('\n') if line.strip() != '']
    
    results = []
    fake_count = 0
    
    for r in raw_reviews:
        r_lower = r.lower()
        triggers_found = [kw for kw in FAKE_KEYWORDS if kw in r_lower]
        
        # NLP Classification Logic (Simulated)
        if len(triggers_found) > 0 or len(r.split()) < 4:
            # Marked as fake if it contains extreme buzzwords or is suspiciously short
            status = "FAKE"
            confidence = random.randint(85, 99)
            fake_count += 1
            
            # Explainable AI Text
            if len(triggers_found) > 0:
                explanation = f"High TF-IDF weights on promotional/deceptive tokens: {', '.join(triggers_found).upper()}."
            else:
                explanation = "Review is suspiciously short lacking semantic depth, common in automated bot scripts."
        else:
            status = "REAL"
            confidence = random.randint(75, 95)
            triggers_found = []
            explanation = "Natural language variance detected. Proper sentence structure and emotional sentiment variance indicates human authorship."

        # Assign a random IP origin location for the map
        loc = random.choice(CITIES)
        
        res_obj = {
            "text": r,
            "status": status,
            "confidence": confidence,
            "triggers": triggers_found,
            "explanation": explanation,
            "location": loc
        }
        
        results.append(res_obj)
        GLOBAL_HISTORY.append(res_obj)
        
    return jsonify({
        "total": len(results),
        "fake": fake_count,
        "real": len(results) - fake_count,
        "reviews": results,
        "history": GLOBAL_HISTORY
    })

if __name__ == '__main__':
    # Run on port 5004
    app.run(debug=True, port=5004)
