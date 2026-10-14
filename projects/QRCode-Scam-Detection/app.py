import os
import random
from flask import Flask, render_template, request, jsonify, redirect, url_for

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Cyber-security simulation mock data
MALICIOUS_DOMAINS = ['login-update-paypal.com', 'secure-bank-alert.net', 'free-bitcoin-giveaway.org', 'scam-site.info']

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

@app.route('/api/scan_qr', methods=['POST'])
def scan_qr():
    url_input = request.form.get('url_text', '')
    
    # If file was uploaded instead of URL, simulate decoding it
    if not url_input and 'qr_image' in request.files:
        file = request.files['qr_image']
        if file.filename:
            # Simulate decoding a random malicious or safe URL
            url_input = random.choice(['https://secure-bank-alert.net/login', 'https://www.google.com', 'https://free-bitcoin-giveaway.org/claim'])

    if not url_input.strip():
        return jsonify({"error": "No URL or QR image provided."}), 400

    url_lower = url_input.lower()
    
    # AI Risk Analysis Simulation
    is_malicious = any(domain in url_lower for domain in MALICIOUS_DOMAINS)
    
    if is_malicious:
        risk_level = "MALICIOUS"
        confidence = random.randint(85, 99)
        risk_factors = ["Suspicious TLD", "Known Blacklisted Domain", "Phishing Signature Detected"]
    else:
        # Check if it's suspicious based on length or HTTP (not HTTPS)
        if url_lower.startswith('http://') or len(url_lower) > 50:
            risk_level = "SUSPICIOUS"
            confidence = random.randint(50, 80)
            risk_factors = ["Lack of SSL (HTTP)", "Unusual URL Length"]
        else:
            risk_level = "SAFE"
            confidence = random.randint(90, 99)
            risk_factors = ["Valid SSL", "Domain Age > 5 Years", "No Blacklist Records"]

    return jsonify({
        "url": url_input,
        "risk_level": risk_level,
        "confidence": confidence,
        "risk_factors": risk_factors
    })

@app.route('/api/submit_feedback', methods=['POST'])
def submit_feedback():
    return jsonify({"success": True, "message": "Feedback submitted to improve AI model."})

if __name__ == '__main__':
    # Run on port 5002
    app.run(debug=True, port=5002)
