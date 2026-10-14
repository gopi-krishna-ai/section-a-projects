import os

base_dir = r'C:\Users\krish\OneDrive\Desktop\section a\01_GuardPath_AI_Updated\B-1-GuardPath AI'
app_path = os.path.join(base_dir, 'app.py')

with open(app_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the sos_alert route
old_sos = '''@app.route("/sos_alert", methods=["POST"])
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
    
    return jsonify({'success': True, 'message': 'SOS sent to trusted contacts!'})'''

new_sos = '''@app.route("/sos_alert", methods=["POST"])
def sos_alert():
    if 'user' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
        
    data = request.get_json() or {}
    lat = data.get('lat', 'Unknown')
    lng = data.get('lng', 'Unknown')
    email = data.get('email', 'No Email Provided')
    message = data.get('message', 'Emergency SOS Triggered')
    
    user = session['user']
    
    alert = {
        'id': str(uuid.uuid4()),
        'user': user,
        'name': session.get('name', 'User'),
        'lat': lat,
        'lng': lng,
        'email': email,
        'message': message,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    SOS_ALERTS.append(alert)
    # Simulate sending Email
    print(f"\\n{'='*40}\\n🚨 URGENT SOS EMAIL SENT 🚨\\nTo: {email}\\nFrom: GuardPath Safety System\\nUser: {alert['name']}\\nLocation: LAT {lat}, LNG {lng}\\nMessage: {message}\\n{'='*40}\\n")
    
    return jsonify({'success': True, 'message': f'SOS Alert and Live Location successfully sent to {email}!'})'''

content = content.replace(old_sos, new_sos)

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated SOS route in app.py")
