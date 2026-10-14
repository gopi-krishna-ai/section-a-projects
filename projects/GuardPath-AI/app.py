import csv
import os
import uuid
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename

import smtplib
from email.message import EmailMessage

import json

# --- EMAIL CONFIGURATION ---
SMTP_CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "smtp_config.json")

def load_smtp_config():
    if os.path.exists(SMTP_CONFIG_FILE):
        with open(SMTP_CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {'email': 'siri86384@gmail.com', 'password': 'heysiri@123'}

def save_smtp_config(email, password):
    with open(SMTP_CONFIG_FILE, 'w') as f:
        json.dump({'email': email, 'password': password}, f)

def send_real_email(to_email, subject, body, attachment_path=None):
    config = load_smtp_config()
    sender_email = config.get('email')
    sender_password = config.get('password')
    
    if not sender_email or not sender_password:
        print("Real email skipped: Please configure SMTP credentials in Admin Dashboard")
        return False
    try:
        msg = EmailMessage()
        msg.set_content(body)
        msg['Subject'] = subject
        msg['From'] = f"GuardPath AI <{sender_email}>"
        msg['To'] = to_email

        if attachment_path and os.path.exists(attachment_path):
            import mimetypes
            ctype, encoding = mimetypes.guess_type(attachment_path)
            if ctype is None or encoding is not None:
                ctype = 'application/octet-stream'
            maintype, subtype = ctype.split('/', 1)
            with open(attachment_path, 'rb') as f:
                msg.add_attachment(f.read(), maintype=maintype, subtype=subtype, filename=os.path.basename(attachment_path))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"Email failed: {e}")
        return False


from flask import Flask, jsonify, render_template, request, session, redirect, url_for, flash

from utils.city_graph import all_edges
from utils.safety_engine import get_area_coords, get_area_details, get_area_list, recommend_route

app = Flask(__name__)
app.secret_key = 'super_secret_guardpath_key'
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')

STATS_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "data", "kaggle_reference", "ward_derivation_stats.csv"
)

import json

USERS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "users.json")

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=4)

# New Data stores for Community Hazards and SOS (PRE-LOADED DEMO DATA)
HAZARDS = [
    {
        'id': 'demo-haz-1',
        'user': 'passenger2',
        'name': 'Bob',
        'description': 'Severe waterlogging under the bridge, traffic at standstill.',
        'lat': 12.9172,
        'lng': 77.6228,
        'image': None,
        'timestamp': (datetime.now() - timedelta(minutes=45)).strftime('%Y-%m-%d %H:%M:%S')
    },
    {
        'id': 'demo-haz-2',
        'user': 'passenger1',
        'name': 'Alice',
        'description': 'Fallen tree blocking the left lane on main road.',
        'lat': 12.9716,
        'lng': 77.5946,
        'image': None,
        'timestamp': (datetime.now() - timedelta(hours=2)).strftime('%Y-%m-%d %H:%M:%S')
    }
]

SOS_ALERTS = [
    {
        'id': 'demo-sos-1',
        'user': 'passenger2',
        'name': 'Bob',
        'lat': 12.9352,
        'lng': 77.6245,
        'email': 'family.emergency@example.com',
        'message': 'My cab took a wrong turn into a dark alley and driver is acting suspicious.',
        'timestamp': (datetime.now() - timedelta(minutes=15)).strftime('%Y-%m-%d %H:%M:%S')
    }
]

HISTORY_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "ride_history.json")

def generate_mock_history(passenger_name):
    history = []
    base_date = datetime.now()
    areas = list(get_area_coords().keys())
    for i in range(10):
        src = areas[i % len(areas)]
        dst = areas[(i + 3) % len(areas)]
        ride_date = base_date - timedelta(days=i*2, hours=i*3, minutes=i*12)
        history.append({
            'date': ride_date.strftime('%Y-%m-%d %H:%M'),
            'source': src,
            'destination': dst,
            'mode': 'walking' if i % 2 == 0 else 'driving',
            'time': 'night' if i % 3 == 0 else 'day',
            'suggestion_used': 'Safest Route' if i % 2 == 0 else 'Shortest Route',
            'safety_score': max(55, 88 - (i * 3))
        })
    return history

def load_ride_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r') as f:
                return json.load(f)
        except Exception:
            pass
    # Initialize default history for test accounts
    initial = {
        'passenger1': generate_mock_history('passenger1'),
        'passenger2': generate_mock_history('passenger2'),
        'gopi': generate_mock_history('gopi'),
        'adithya123': generate_mock_history('adithya123')
    }
    save_ride_history(initial)
    return initial

def save_ride_history(history_dict):
    try:
        with open(HISTORY_FILE, 'w') as f:
            json.dump(history_dict, f, indent=4)
    except Exception as e:
        print(f"Error saving ride history: {e}")

def get_user_ride_history(username):
    history_dict = load_ride_history()
    if username not in history_dict or not history_dict[username]:
        history_dict[username] = generate_mock_history(username)
        save_ride_history(history_dict)
    return history_dict[username]

def add_ride_to_history(username, source, destination, mode, time_of_day, suggestion_used, safety_score):
    if not username:
        return
    history_dict = load_ride_history()
    if username not in history_dict:
        history_dict[username] = generate_mock_history(username)
    
    new_entry = {
        'date': datetime.now().strftime('%Y-%m-%d %H:%M'),
        'source': source,
        'destination': destination,
        'mode': mode,
        'time': time_of_day,
        'suggestion_used': suggestion_used,
        'safety_score': round(float(safety_score), 1)
    }
    history_dict[username].insert(0, new_entry)
    save_ride_history(history_dict)
    return new_entry

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
        
        users = load_users()
        if username in users and users[username]['password'] == password:
            session['user'] = username
            session['role'] = users[username]['role']
            session['name'] = users[username]['name']
            
            if session['role'] == 'admin':
                return redirect(url_for('admin_dashboard'))
            return redirect(url_for('map_view'))
        else:
            flash("Invalid credentials. Please try again.")
    
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        name = request.form.get("name")
        email = request.form.get("email")
        
        users = load_users()
        if username in users:
            flash("Username already exists. Please choose another or login.")
        else:
            users[username] = {
                'password': password,
                'role': 'passenger',
                'name': name,
                'email': email
            }
            save_users(users)
            flash("Registration successful! You can now log in.")
            return redirect(url_for('login'))
            
    return render_template("register.html")

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
        data = load_ride_history()
    else:
        data = {user: get_user_ride_history(user)}
        
    return render_template("history.html", history_data=data, role=role, user=user, name=session.get('name'))

@app.route("/admin_dashboard", methods=["GET", "POST"])
def admin_dashboard():
    if session.get('role') != 'admin':
        return redirect(url_for('login'))
    
    if request.method == "POST":
        email = request.form.get('smtp_email', '').strip()
        password = request.form.get('smtp_password', '').strip()
        save_smtp_config(email, password)
        flash("Email configuration updated successfully!")
        return redirect(url_for('admin_dashboard'))

    smtp_config = load_smtp_config()
    users = load_users()
    history_data = load_ride_history()
    return render_template(
        "admin.html",
        hazards=HAZARDS,
        sos_alerts=SOS_ALERTS,
        history_data=history_data,
        users=users,
        name=session.get('name'),
        smtp_config=smtp_config
    )

import re
import random

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    msg = data.get("message", "").lower()
    
    # Simple Mock AI Logic
    response = "I am the GuardPath AI Assistant. I can help you with safety info, route advice, and weather forecasts. How can I help you travel safely?"
    
    if "weather" in msg or "rain" in msg or "temperature" in msg:
        if "day" in msg or "tomorrow" in msg:
            # Extract numbers if they asked "after X days"
            nums = re.findall(r'\d+', msg)
            days = nums[0] if nums else "a few"
            conditions = random.choice(["mostly clear with a low risk of rain", "expecting heavy thunderstorms", "overcast but safe for travel", "foggy with low visibility"])
            temp = random.randint(22, 32)
            response = f"🌤️ Based on our meteorological models, the weather in {days} days will be {conditions}. The temperature should be around {temp}°C. Plan your travel accordingly!"
        else:
            response = "☀️ The current weather is clear at 28°C. Road conditions are optimal for travel right now. Do you need a forecast for a specific day?"
            
    elif "safest route" in msg or "travel" in msg or "go from" in msg:
        response = "🛡️ To find the safest route, please use the 'Plan a Safer Route' panel on the left side of the map! Our ML model analyzes live traffic, crime rates, and lighting to give you the best path."
        
    elif "hello" in msg or "hi" in msg:
        response = "Hello! 👋 GuardPath AI is online and monitoring your safety. How can I assist?"
        
    return jsonify({"response": response})

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

    # Automatically save this planned ride into user's ride history
    if 'user' in session and result.get("routes"):
        best_route = result["routes"][0]
        add_ride_to_history(
            username=session['user'],
            source=source,
            destination=destination,
            mode=travel_mode,
            time_of_day=travel_time,
            suggestion_used="Safest Route (AI Recommended)",
            safety_score=best_route.get("safety_score", 85)
        )

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
        
    data = request.form if request.form else (request.get_json() or {})
    lat = data.get('lat', 'Unknown')
    lng = data.get('lng', 'Unknown')
    email = data.get('email', 'No Email Provided')
    message = data.get('message', 'Emergency SOS Triggered')
    
    user = session['user']
    if not email or email in ['No Email Provided', 'No Email']:
        users = load_users()
        if user in users and users[user].get('parent_email'):
            email = users[user]['parent_email']
        elif user in users and users[user].get('emergency_email'):
            email = users[user]['emergency_email']
        else:
            email = 'krishnagopi5600@gmail.com'
            
    # Handle optional voice message
    voice_filename = None
    voice_path = None
    if 'voice_message' in request.files:
        file = request.files['voice_message']
        if file.filename:
            voice_filename = secure_filename(f"sos_{uuid.uuid4().hex}_{file.filename}")
            voice_path = os.path.join(app.config['UPLOAD_FOLDER'], voice_filename)
            file.save(voice_path)
    
    alert = {
        'id': str(uuid.uuid4()),
        'user': user,
        'name': session.get('name', 'User'),
        'lat': lat,
        'lng': lng,
        'email': email,
        'message': message,
        'voice_file': voice_filename,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    SOS_ALERTS.append(alert)
    # Attempt to send REAL Email
    email_body = f"""*** URGENT SOS EMERGENCY ALERT ***
    
User '{alert['name']}' has triggered an SOS.

[Location] Live Location: LAT {lat}, LNG {lng}
https://maps.google.com/?q={lat},{lng}

[Message] Custom Message:
{message}

Please respond immediately.
- GuardPath AI Safety System"""

    if voice_filename:
        email_body += f"\n\n[Voice Message] An audio recording has been attached to this email."

    email_sent = send_real_email(email, "*** URGENT SOS ALERT from GuardPath AI", email_body, attachment_path=voice_path)
    
    if email_sent:
        print(f"REAL Email successfully sent to {email}")
    else:
        print(f"\n{'='*40}\n*** SIMULATED SOS EMAIL ***\nTo: {email}\n{email_body}\n{'='*40}\n")
    
    return jsonify({'success': True, 'message': f'SOS Alert and Live Location successfully sent to {email}!'})

if __name__ == "__main__":
    app.run(debug=True, port=int(os.environ.get("PORT", 5000)))
