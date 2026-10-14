import os

app_path = 'app.py'
with open(app_path, 'r', encoding='utf-8') as f:
    content = f.read()

api_logic = '''
DISASTER_FILE = 'data/disasters.json'

@app.route('/api/disasters', methods=['GET', 'POST'])
def manage_disasters():
    if request.method == 'GET':
        if not os.path.exists(DISASTER_FILE):
            return jsonify([])
        with open(DISASTER_FILE, 'r') as f:
            return jsonify(json.load(f))
            
    if request.method == 'POST':
        data = request.json
        if not os.path.exists(DISASTER_FILE):
            disasters = []
        else:
            with open(DISASTER_FILE, 'r') as f:
                disasters = json.load(f)
                
        new_disaster = {
            "year": 2026,  # Present year
            "lat": float(data.get('lat')),
            "lng": float(data.get('lng')),
            "country": data.get('country', 'Unknown Location'),
            "type": data.get('type', 'Reported Incident'),
            "deaths": int(data.get('deaths', 0)),
            "desc": data.get('desc', 'User submitted report.')
        }
        disasters.append(new_disaster)
        
        with open(DISASTER_FILE, 'w') as f:
            json.dump(disasters, f)
            
        return jsonify({"status": "success", "message": "Disaster added"})
'''

if '@app.route(\'/api/disasters\'' not in content:
    # Insert it right before the chat API
    content = content.replace("@app.route('/api/chat', methods=['POST'])", api_logic + "\n@app.route('/api/chat', methods=['POST'])")
    
    with open(app_path, 'w', encoding='utf-8') as f:
        f.write(content)
