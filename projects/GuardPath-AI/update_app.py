import os

base_dir = r'C:\Users\krish\OneDrive\Desktop\section a\01_GuardPath_AI_Updated\B-1-GuardPath AI'
app_path = os.path.join(base_dir, 'app.py')

app_code = '''import csv
import os
import uuid
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename

from flask import Flask, jsonify, render_template, request, session, redirect, url_for, flash

from utils.city_graph import all_edges
from utils.safety_engine import get_area_coords, get_area_details, get_area_list, recommend_route

app = Flask(__name__)
app.secret_key = 'super_secret_guardpath_key'
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')

STATS_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "data", "kaggle_reference", "ward_derivation_stats.csv"
)

# Mock Data for Users and History
USERS = {
    'admin': {'password': 'admin', 'role': 'admin', 'name': 'System Admin'},
    'passenger1': {'password': 'pass1', 'role': 'passenger', 'name': 'Alice', 'contacts': ['+1234567890']},
    'passenger2': {'password': 'pass2', 'role': 'passenger', 'name': 'Bob', 'contacts': ['+0987654321']}
}

# New Data stores for Community Hazards and SOS
HAZARDS = []
SOS_ALERTS = []

def generate_mock_history(passenger_name):
    history = []
    base_date = datetime.now()
    areas = list(get_area_coords().keys())
    for i in range(10):
        src = areas[i % len(areas)]
        dst = areas[(i + 3) % len(areas)]
        ride_date = base_date - timedelta(days=i*2)
        history.append({
            'date': ride_date.strftime('%Y-%m-%d %H:%M'),
            'source': src,
            'destination': dst,
            'mode': 'walking' if i % 2 == 0 else 'driving',
            'time': 'night' if i % 3 == 0 else 'day',
            'suggestion_used': 'Safest Route' if i % 2 == 0 else 'Shortest Route',
            'safety_score': 85 - (i * 2)
        })
    return history

MOCK_HISTORY = {
    'passenger1': generate_mock_history('passenger1'),
    'passenger2': generate_mock_history('passenger2')
}

def _load_alert_counts():
    counts = {}
    if os.path.exists(STATS_PATH):
        with open(STATS_PATH, newline="") as f:
            for row in csv.DictReader(f):
                counts[row["area_name"]] = int(row["alert_count"])
    return counts

@app.route("/")
def landing():
    return render_template("landing.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        if username in USERS and USERS[username]['password'] == password:
            session['user'] = username
            session['role'] = USERS[username]['role']
            session['name'] = USERS[username]['name']
            
            if session['role'] == 'admin':
                return redirect(url_for('admin_dashboard'))
            return redirect(url_for('map_view'))
        else:
            flash("Invalid credentials. Please try again.")
    
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('landing'))

@app.route("/map")
def map_view():
    if 'user' not in session or session.get('role') != 'passenger':
        return redirect(url_for('login'))

    areas = get_area_list()
    area_coords = get_area_coords()
    network_edges = all_edges()

    area_info = get_area_details()
    alert_counts = _load_alert_counts()
    for name, info in area_info.items():
        info["alert_count"] = alert_counts.get(name)

    return render_template(
        "map.html",
        areas=areas,
        area_coords=area_coords,
        network_edges=network_edges,
        area_info=area_info,
        user=session.get('user'),
        role=session.get('role'),
        name=session.get('name')
    )

@app.route("/history")
def history():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    user = session['user']
    role = session['role']
    
    if role == 'admin':
        data = MOCK_HISTORY
    else:
        data = {user: MOCK_HISTORY.get(user, [])}
        
    return render_template("history.html", history_data=data, role=role, user=user, name=session.get('name'))

@app.route("/admin_dashboard")
def admin_dashboard():
    if session.get('role') != 'admin':
        return redirect(url_for('login'))
    
    return render_template("admin.html", hazards=HAZARDS, sos_alerts=SOS_ALERTS, history_data=MOCK_HISTORY, name=session.get('name'))

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json(silent=True) or request.form
    source = (data.get("source") or "").strip()
    destination = (data.get("destination") or "").strip()
    travel_time = (data.get("travel_time") or "day").strip().lower()
    travel_mode = (data.get("travel_mode") or "walking").strip().lower()

    if not source or not destination:
        return jsonify({"error": "Please select both a source and a destination."}), 400

    result = recommend_route(source, destination, travel_time, travel_mode)
    if "error" in result:
        return jsonify(result), 400

    return jsonify(result)

# --- NEW API ROUTES FOR ADDED FEATURES ---

@app.route("/upload_hazard", methods=["POST"])
def upload_hazard():
    if 'user' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    desc = request.form.get('description', '')
    lat = request.form.get('lat')
    lng = request.form.get('lng')
    image = request.files.get('image')
    
    if not lat or not lng:
        return jsonify({'error': 'Location required'}), 400
        
    filename = None
    if image:
        filename = str(uuid.uuid4()) + "_" + secure_filename(image.filename)
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
    hazard = {
        'id': str(uuid.uuid4()),
        'user': session['user'],
        'name': session.get('name', 'User'),
        'description': desc,
        'lat': float(lat),
        'lng': float(lng),
        'image': filename,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    HAZARDS.append(hazard)
    return jsonify({'success': True, 'hazard': hazard})

@app.route("/get_hazards", methods=["GET"])
def get_hazards():
    return jsonify(HAZARDS)

@app.route("/sos_alert", methods=["POST"])
def sos_alert():
    if 'user' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
        
    data = request.get_json() or {}
    lat = data.get('lat', 'Unknown')
    lng = data.get('lng', 'Unknown')
    reason = data.get('reason', 'Emergency Button Pressed')
    
    user = session['user']
    contacts = USERS.get(user, {}).get('contacts', [])
    
    alert = {
        'id': str(uuid.uuid4()),
        'user': user,
        'name': session.get('name', 'User'),
        'lat': lat,
        'lng': lng,
        'reason': reason,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'contacts_notified': contacts
    }
    SOS_ALERTS.append(alert)
    # Simulate sending SMS
    print(f"SOS SENT TO: {contacts}. Location: {lat},{lng}. User: {alert['name']}")
    
    return jsonify({'success': True, 'message': 'SOS sent to trusted contacts!'})

if __name__ == "__main__":
    app.run(debug=True, port=int(os.environ.get("PORT", 5000)))
'''

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(app_code)

print("Updated app.py")
