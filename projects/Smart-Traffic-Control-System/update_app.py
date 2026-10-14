import os
import re

base_dir = r'C:\Users\krish\OneDrive\Desktop\section a\TrafficControlSystem'
app_path = os.path.join(base_dir, 'app.py')

with open(app_path, 'r', encoding='utf-8') as f:
    content = f.read()

ml_imports = '''import joblib
from datetime import datetime

# Load ML Model
model_path = os.path.join('ml', 'models', 'green_time_model.pkl')
if os.path.exists(model_path):
    traffic_model = joblib.load(model_path)
else:
    traffic_model = None
'''

content = content.replace("from flask import Flask", ml_imports + "\nfrom flask import Flask")

old_analyze = '''@app.route('/api/analyze_traffic', methods=['POST'])
def analyze_traffic():
    global current_threshold
    # Mocking YOLO detection on an uploaded video
    # Return random vehicle count between 2 and 25
    vehicle_count = random.randint(2, 25)
    
    # Logic: > threshold = RED, <= threshold = GREEN
    if vehicle_count > current_threshold:
        signal_color = "RED"
        status = "Highly Congested"
    else:
        signal_color = "GREEN"
        status = "Normal Flow"

    # Mock image of YOLO bounding boxes
    mock_processed_image = "https://images.unsplash.com/photo-1542385151-efd9000785a0?w=800&q=80" # Busy intersection image

    return jsonify({
        "count": vehicle_count,
        "signal": signal_color,
        "status": status,
        "threshold": current_threshold,
        "image": mock_processed_image
    })'''

new_analyze = '''@app.route('/api/analyze_traffic', methods=['POST'])
def analyze_traffic():
    global current_threshold
    # Mocking YOLO detection on an uploaded video
    # Return random vehicle count between 2 and 45 to show ML range
    vehicle_count = random.randint(2, 45)
    
    # Logic: > threshold = RED, <= threshold = GREEN
    if vehicle_count > current_threshold:
        signal_color = "RED"
        status = "Highly Congested"
    else:
        signal_color = "GREEN"
        status = "Normal Flow"
        
    # --- NEW ML LOGIC ---
    ml_prediction = "N/A"
    if traffic_model:
        # Features: hour (0-23), day_of_week (0-6), weather (0=Clear, 1=Rain, 2=Fog), vehicle_count (0-100)
        now = datetime.now()
        hour = now.hour
        day_of_week = now.weekday()
        weather = 0 # Assume Clear for demo, could be fetched dynamically
        
        # Predict optimal green time
        pred = traffic_model.predict([[hour, day_of_week, weather, vehicle_count]])[0]
        ml_prediction = f"{int(pred)} Seconds"

    # Mock image of YOLO bounding boxes
    mock_processed_image = "https://images.unsplash.com/photo-1542385151-efd9000785a0?w=800&q=80" # Busy intersection image

    return jsonify({
        "count": vehicle_count,
        "signal": signal_color,
        "status": status,
        "threshold": current_threshold,
        "image": mock_processed_image,
        "ml_optimal_time": ml_prediction
    })'''

content = content.replace(old_analyze, new_analyze)

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(content)
