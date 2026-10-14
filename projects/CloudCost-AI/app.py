import os
from flask import Flask, render_template, request, jsonify, redirect, url_for

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# 10 Built-in Demos
DEMO_VMS = [
    {"id": "aws-web-prod-01", "provider": "AWS", "region": "Mumbai", "lat": 19.0760, "lon": 72.8777, "cpu": 85, "ram": "16GB", "storage": "500GB SSD", "network": "High", "cost": 150, "status": "Optimal", "action": "None"},
    {"id": "aws-db-legacy-04", "provider": "AWS", "region": "Mumbai", "lat": 19.1, "lon": 72.9, "cpu": 4, "ram": "32GB", "storage": "2TB HDD", "network": "Low", "cost": 320, "status": "Idle", "action": "Shutdown"},
    {"id": "az-worker-node-1", "provider": "Azure", "region": "Pune", "lat": 18.5204, "lon": 73.8567, "cpu": 12, "ram": "64GB", "storage": "1TB SSD", "network": "Med", "cost": 180, "status": "Underutilized", "action": "Downsize (Save $90/mo)"},
    {"id": "az-api-gateway", "provider": "Azure", "region": "Pune", "lat": 18.55, "lon": 73.9, "cpu": 78, "ram": "8GB", "storage": "100GB SSD", "network": "High", "cost": 95, "status": "Optimal", "action": "None"},
    {"id": "gcp-data-pipeline", "provider": "GCP", "region": "Delhi", "lat": 28.7041, "lon": 77.1025, "cpu": 95, "ram": "128GB", "storage": "5TB NVMe", "network": "Max", "cost": 410, "status": "Overloaded", "action": "Scale Up"},
    {"id": "gcp-test-env-01", "provider": "GCP", "region": "Delhi", "lat": 28.6, "lon": 77.2, "cpu": 1, "ram": "4GB", "storage": "50GB HDD", "network": "Zero", "cost": 65, "status": "Idle", "action": "Shutdown (Save $65/mo)"},
    {"id": "aws-cache-redis", "provider": "AWS", "region": "Hyderabad", "lat": 17.3850, "lon": 78.4867, "cpu": 18, "ram": "16GB", "storage": "20GB SSD", "network": "High", "cost": 210, "status": "Underutilized", "action": "Downsize (Save $110/mo)"},
    {"id": "az-ml-training", "provider": "Azure", "region": "Chennai", "lat": 13.0827, "lon": 80.2707, "cpu": 99, "ram": "256GB", "storage": "10TB NVMe", "network": "Max", "cost": 850, "status": "Optimal", "action": "None"},
    {"id": "gcp-backup-server", "provider": "GCP", "region": "Bangalore", "lat": 12.9716, "lon": 77.5946, "cpu": 2, "ram": "32GB", "storage": "50TB HDD", "network": "Med", "cost": 300, "status": "Idle", "action": "Migrate to Cold Storage"},
    {"id": "aws-staging-web", "provider": "AWS", "region": "Bangalore", "lat": 13.0, "lon": 77.6, "cpu": 8, "ram": "8GB", "storage": "200GB SSD", "network": "Low", "cost": 120, "status": "Underutilized", "action": "Shutdown after hours"}
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

@app.route('/api/analyze_cloud', methods=['POST', 'GET'])
def analyze_cloud():
    # Calculate costs
    current_cost = sum(vm['cost'] for vm in DEMO_VMS)
    
    # Calculate optimized cost (subtracting savings)
    optimized_cost = current_cost
    for vm in DEMO_VMS:
        if "Save $" in vm['action']:
            try:
                savings = int(vm['action'].split('Save $')[1].split('/')[0])
                optimized_cost -= savings
            except:
                pass
        elif vm['action'] == "Shutdown":
            optimized_cost -= vm['cost']
        elif "Cold Storage" in vm['action']:
            optimized_cost -= (vm['cost'] - 20) # 20 is cost of cold storage
            
    return jsonify({
        "vms": DEMO_VMS,
        "current_total": current_cost,
        "optimized_total": optimized_cost,
        "waste": current_cost - optimized_cost
    })

@app.route('/api/add_vm', methods=['POST'])
def add_vm():
    new_vm = {
        "id": request.form.get('id', 'manual-instance'),
        "provider": request.form.get('provider', 'Custom'),
        "region": request.form.get('region', 'Unknown'),
        "lat": float(request.form.get('lat', 20.0)),
        "lon": float(request.form.get('lon', 78.0)),
        "cpu": int(request.form.get('cpu', 50)),
        "ram": request.form.get('ram', '16GB'),
        "storage": request.form.get('storage', '100GB'),
        "network": "Med",
        "cost": int(request.form.get('cost', 100))
    }
    
    # Simple AI logic for the new VM
    if new_vm['cpu'] < 10:
        new_vm['status'] = "Idle"
        new_vm['action'] = f"Shutdown (Save ${new_vm['cost']}/mo)"
    elif new_vm['cpu'] < 40:
        new_vm['status'] = "Underutilized"
        new_vm['action'] = f"Downsize (Save ${int(new_vm['cost']/2)}/mo)"
    elif new_vm['cpu'] > 90:
        new_vm['status'] = "Overloaded"
        new_vm['action'] = "Scale Up"
    else:
        new_vm['status'] = "Optimal"
        new_vm['action'] = "None"

    DEMO_VMS.append(new_vm)
    return jsonify({"success": True})

if __name__ == '__main__':
    # Run on port 5003
    app.run(debug=True, port=5003)
