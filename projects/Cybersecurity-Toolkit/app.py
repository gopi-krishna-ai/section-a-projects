import os
import hashlib
import re
import socket
import urllib.parse
import sqlite3
import random
import datetime
import string
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session, send_file
import joblib
import tldextract
from werkzeug.security import generate_password_hash, check_password_hash
from fpdf import FPDF

app = Flask(__name__)
app.secret_key = 'cybersecurity_toolkit_secret'

# Load ML Model for Phishing Detection
model_path = os.path.join(os.path.dirname(__file__), 'model', 'phishing_model.pkl')
phishing_model = None
try:
    if os.path.exists(model_path):
        phishing_model = joblib.load(model_path)
    else:
        print("Warning: Phishing model not found. Please run model/train_model.py first.")
except Exception as e:
    print(f"Error loading model: {e}")

# Database connection and initialization
def get_db_connection():
    db_path = os.path.join(os.path.dirname(__file__), 'database.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS login_attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            ip_address TEXT,
            status TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS scan_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            scan_type TEXT NOT NULL,
            target TEXT NOT NULL,
            result TEXT NOT NULL,
            risk_level TEXT NOT NULL,
            score INTEGER NOT NULL,
            status TEXT NOT NULL,
            solution TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Insert default admin and user
    admin = conn.execute("SELECT * FROM users WHERE username = 'admin'").fetchone()
    if not admin:
        conn.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", 
                     ('admin', generate_password_hash('admin123'), 'admin'))
    user = conn.execute("SELECT * FROM users WHERE username = 'user'").fetchone()
    if not user:
        conn.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", 
                     ('user', generate_password_hash('user123'), 'user'))
    conn.commit()
    conn.close()

init_db()

# Decorators for auth
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or not session.get('otp_verified'):
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('role') != 'admin' or not session.get('otp_verified'):
            flash("Admin access required.", "danger")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def log_login_attempt(username, ip_address, status):
    conn = get_db_connection()
    conn.execute("INSERT INTO login_attempts (username, ip_address, status) VALUES (?, ?, ?)",
                 (username, ip_address, status))
    conn.commit()
    conn.close()

def log_scan(scan_type, target, result, risk_level, score, status, solution):
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO scan_history (scan_type, target, result, risk_level, score, status, solution)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (scan_type, target, str(result), risk_level, score, status, solution))
    conn.commit()
    conn.close()

# --- Auth Routes ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        conn.close()
        
        if user and check_password_hash(user['password'], password):
            log_login_attempt(username, request.remote_addr, "Success")
            session['pending_user_id'] = user['id']
            session['pending_role'] = user['role']
            session['pending_username'] = user['username']
            
            # Generate OTP
            otp = str(random.randint(100000, 999999))
            session['otp'] = otp
            print(f"--- OTP for {username}: {otp} ---") # Console logging
            flash(f"OTP has been generated (Check console: {otp})", "info") # Screen flashing for testing
            
            return redirect(url_for('otp'))
        else:
            log_login_attempt(username, request.remote_addr, "Failed")
            flash("Invalid credentials.", "danger")
            
    return render_template('login.html', is_admin=False)

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE username = ? AND role = 'admin'", (username,)).fetchone()
        conn.close()
        
        if user and check_password_hash(user['password'], password):
            log_login_attempt(username, request.remote_addr, "Success (Admin)")
            session['pending_user_id'] = user['id']
            session['pending_role'] = user['role']
            session['pending_username'] = user['username']
            
            otp = str(random.randint(100000, 999999))
            session['otp'] = otp
            print(f"--- ADMIN OTP for {username}: {otp} ---")
            flash(f"Admin OTP has been generated (Check console: {otp})", "info")
            
            return redirect(url_for('otp'))
        else:
            log_login_attempt(username, request.remote_addr, "Failed (Admin)")
            flash("Invalid admin credentials.", "danger")
            
    return render_template('login.html', is_admin=True)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        
        if user:
            conn.close()
            flash("Username already exists. Please choose a different one.", "danger")
        else:
            conn.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", 
                         (username, generate_password_hash(password), 'user'))
            conn.commit()
            conn.close()
            flash("Registration successful! Please login.", "success")
            return redirect(url_for('login'))
            
    return render_template('register.html', is_admin=False)

@app.route('/admin/register', methods=['GET', 'POST'])
def admin_register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        
        if user:
            conn.close()
            flash("Username already exists. Please choose a different one.", "danger")
        else:
            conn.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", 
                         (username, generate_password_hash(password), 'admin'))
            conn.commit()
            conn.close()
            flash("Admin registration successful! Please login.", "success")
            return redirect(url_for('admin_login'))
            
    return render_template('register.html', is_admin=True)

@app.route('/otp', methods=['GET', 'POST'])
def otp():
    if 'pending_user_id' not in session:
        return redirect(url_for('login'))
        
    if request.method == 'POST':
        user_otp = request.form['otp']
        if user_otp == session.get('otp'):
            session['user_id'] = session['pending_user_id']
            session['role'] = session['pending_role']
            session['username'] = session['pending_username']
            session['otp_verified'] = True
            
            # Clean up pending session vars
            session.pop('pending_user_id', None)
            session.pop('pending_role', None)
            session.pop('pending_username', None)
            session.pop('otp', None)
            
            flash("Login successful!", "success")
            if session['role'] == 'admin':
                return redirect(url_for('admin_dashboard'))
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid OTP.", "danger")
            
    return render_template('otp.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for('landing'))

# --- Admin Routes ---
@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    conn = get_db_connection()
    total_scans = conn.execute("SELECT COUNT(*) FROM scan_history").fetchone()[0]
    total_malware = conn.execute("SELECT COUNT(*) FROM scan_history WHERE status = 'Harmful'").fetchone()[0]
    login_attempts = conn.execute("SELECT * FROM login_attempts ORDER BY timestamp DESC LIMIT 50").fetchall()
    conn.close()
    
    return render_template('admin_dashboard.html', total_scans=total_scans, 
                           total_malware=total_malware, login_attempts=login_attempts)

# --- Core Routes ---
@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/dashboard')
@login_required
def dashboard():
    conn = get_db_connection()
    total_scans = conn.execute("SELECT COUNT(*) FROM scan_history").fetchone()[0]
    total_malware = conn.execute("SELECT COUNT(*) FROM scan_history WHERE status = 'Harmful'").fetchone()[0]
    conn.close()
    return render_template('index.html', total_scans=total_scans, total_malware=total_malware)

@app.route('/password', methods=['GET', 'POST'])
@login_required
def password_check():
    result = None
    if request.method == 'POST':
        password = request.form['password']
        score = 0
        feedback = []

        if len(password) >= 8: score += 1
        else: feedback.append("Password should be at least 8 characters long.")
        
        if re.search(r"[a-z]", password) and re.search(r"[A-Z]", password): score += 1
        else: feedback.append("Include both lowercase and uppercase letters.")
        
        if re.search(r"\d", password): score += 1
        else: feedback.append("Include at least one number.")
        
        if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password): score += 1
        else: feedback.append("Include at least one special character.")

        final_score = (score / 4) * 100
        
        if final_score == 100:
            risk = "Low"
            status = "Safe"
            solution = "No action needed."
        elif final_score >= 50:
            risk = "Medium"
            status = "Moderate"
            solution = "Add special characters or numbers to make it stronger."
        else:
            risk = "High"
            status = "Harmful"
            solution = "Password is too weak. Use a mix of uppercase, lowercase, numbers, and symbols. Minimum 8 characters."
            
        result = {"status": status, "score": int(final_score), "feedback": feedback, "solution": solution}
        log_scan("Password Analysis", "N/A (Hidden)", ", ".join(feedback) if feedback else "Strong", risk, int(final_score), status, solution)
        
    return render_template('password.html', result=result)

@app.route('/password_gen', methods=['GET', 'POST'])
@login_required
def password_gen():
    generated_password = None
    if request.method == 'POST':
        length = int(request.form.get('length', 12))
        use_upper = request.form.get('use_upper')
        use_lower = request.form.get('use_lower')
        use_digits = request.form.get('use_digits')
        use_special = request.form.get('use_special')

        characters = ""
        if use_upper: characters += string.ascii_uppercase
        if use_lower: characters += string.ascii_lowercase
        if use_digits: characters += string.digits
        if use_special: characters += "!@#$%^&*(),.?\":{}|<>"

        if not characters:
            characters = string.ascii_letters + string.digits + "!@#$%^&*()"

        generated_password = ''.join(random.choice(characters) for i in range(length))
        log_scan("Password Gen", "Generated", "Success", "Low", 100, "Safe", "Password Generated Successfully")

    return render_template('password_gen.html', generated_password=generated_password)

@app.route('/hash', methods=['GET', 'POST'])
@login_required
def file_hash():
    result = None
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part', 'danger')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file', 'danger')
            return redirect(request.url)
        if file:
            content = file.read()
            md5_hash = hashlib.md5(content).hexdigest()
            sha1_hash = hashlib.sha1(content).hexdigest()
            sha256_hash = hashlib.sha256(content).hexdigest()
            result = {
                "filename": file.filename,
                "md5": md5_hash,
                "sha1": sha1_hash,
                "sha256": sha256_hash
            }
            log_scan("File Hash Gen", file.filename, "Hashes Generated", "Low", 100, "Safe", "File hashed successfully")
            
    return render_template('hash.html', result=result)

@app.route('/network', methods=['GET', 'POST'])
@login_required
def network_scan():
    result = None
    if request.method == 'POST':
        target_ip = request.form['target_ip']
        ports = [21, 22, 80, 443, 3306, 8080]
        open_ports = []
        
        for port in ports:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            try:
                res = sock.connect_ex((target_ip, port))
                if res == 0:
                    open_ports.append(port)
            except Exception:
                pass
            finally:
                sock.close()
                
        num_open = len(open_ports)
        if num_open == 0:
            score = 100
            status = "Safe"
            risk = "Low"
            solution = "No suspicious open ports detected."
        elif num_open <= 2:
            score = 60
            status = "Moderate"
            risk = "Medium"
            solution = "Review open ports and ensure they are necessary. Use firewalls to restrict access."
        else:
            score = 20
            status = "Harmful"
            risk = "High"
            solution = "Too many open ports. Immediately configure a firewall to block unused ports (e.g., 21, 3306) from public access."

        result = {"target": target_ip, "open_ports": open_ports, "score": score, "status": status, "solution": solution}
        log_scan("Port Scan", target_ip, f"Open Ports: {open_ports}", risk, score, status, solution)
        
    return render_template('network.html', result=result)

@app.route('/url', methods=['GET', 'POST'])
@login_required
def url_check():
    result = None
    if request.method == 'POST':
        url = request.form['url']
        parsed = urllib.parse.urlparse(url)
        
        issues = []
        if parsed.scheme != 'https':
            issues.append("URL does not use HTTPS.")
            
        if len(url) > 75:
            issues.append("URL is unusually long.")
            
        if "@" in url:
            issues.append("URL contains '@' symbol (often used to obscure target).")
            
        if len(issues) == 0:
            score = 100
            status = "Safe"
            risk = "Low"
            solution = "URL looks safe to visit."
        elif len(issues) == 1:
            score = 50
            status = "Moderate"
            risk = "Medium"
            solution = "Proceed with caution. " + " ".join(issues)
        else:
            score = 10
            status = "Harmful"
            risk = "High"
            solution = "Do not visit this URL. " + " ".join(issues)
        
        result = {"url": url, "status": status, "score": score, "issues": issues, "solution": solution}
        log_scan("URL Check", url, status, risk, score, status, solution)
        
    return render_template('url_check.html', result=result)

@app.route('/phishing', methods=['GET', 'POST'])
@login_required
def phishing_detect():
    result = None
    if request.method == 'POST':
        url = request.form['url']
        
        if phishing_model:
            url_length = len(url)
            has_special_chars = 1 if re.search(r"[-@_~?=&]", url) else 0
            
            ext = tldextract.extract(url)
            num_subdomains = len(ext.subdomain.split('.')) if ext.subdomain else 0
            
            is_https = 1 if url.startswith("https") else 0
            
            keywords = ['login', 'verify', 'update', 'secure', 'bank', 'account']
            has_suspicious_keywords = 1 if any(k in url.lower() for k in keywords) else 0
            
            features = [[url_length, has_special_chars, num_subdomains, is_https, has_suspicious_keywords]]
            prediction = phishing_model.predict(features)[0]
            
            if prediction == 1:
                score = 15
                status = "Harmful"
                risk = "High"
                solution = "This is a likely phishing attempt. Do not enter any personal credentials."
            else:
                score = 95
                status = "Safe"
                risk = "Low"
                solution = "URL appears legitimate based on our model."
            
            result = {"url": url, "status": status, "score": score, "features": features[0], "solution": solution}
            log_scan("Phishing Detect", url, status, risk, score, status, solution)
        else:
            flash("Machine learning model is not loaded. Please train it first.", "warning")
            
    return render_template('phishing.html', result=result)

@app.route('/history')
@login_required
def scan_history():
    conn = get_db_connection()
    history = conn.execute("SELECT * FROM scan_history ORDER BY timestamp DESC").fetchall()
    conn.close()
    return render_template('history.html', history=history)

@app.route('/download_report')
@login_required
def download_report():
    conn = get_db_connection()
    # Fetch Moderate and Harmful issues
    issues = conn.execute("SELECT * FROM scan_history WHERE status IN ('Harmful', 'Moderate') ORDER BY timestamp DESC").fetchall()
    conn.close()

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Cybersecurity Toolkit Report", ln=True, align='C')
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 10, txt=f"Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align='C')
    
    pdf.ln(10)
    
    if not issues:
        pdf.cell(200, 10, txt="No moderate or harmful issues found. Great job!", ln=True)
    else:
        for issue in issues:
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(200, 10, txt=f"Scan Type: {issue['scan_type']} | Status: {issue['status']} | Score: {issue['score']}", ln=True)
            pdf.set_font("Arial", size=10)
            pdf.cell(200, 10, txt=f"Target: {issue['target']}", ln=True)
            pdf.cell(200, 10, txt=f"Result: {issue['result']}", ln=True)
            pdf.multi_cell(0, 10, txt=f"Solution: {issue['solution']}")
            pdf.ln(5)

    report_path = os.path.join(os.path.dirname(__file__), 'report.pdf')
    pdf.output(report_path)
    
    return send_file(report_path, as_attachment=True)

@app.route('/chat')
@login_required
def chat():
    return render_template('chat.html')

@app.route('/api/chat', methods=['POST'])
@login_required
def api_chat():
    data = request.json
    message = data.get('message', '').lower()
    
    response = "I'm a cybersecurity assistant. I can help with basic queries about phishing, passwords, ports, or securing your system. Ask me something!"
    
    if 'phishing' in message:
        response = "Phishing is a type of social engineering where an attacker sends a fraudulent message designed to trick a person into revealing sensitive information. Always check the sender's URL and don't click suspicious links."
    elif 'password' in message:
        response = "A strong password should be at least 12 characters long, include uppercase and lowercase letters, numbers, and special characters. Consider using a password manager!"
    elif 'port' in message or 'network' in message:
        response = "Open ports can be a security risk if not properly managed. Ensure you have a firewall blocking unnecessary ports from public access, especially ports like 21 (FTP), 23 (Telnet), and 3306 (MySQL)."
    elif 'malware' in message or 'virus' in message:
        response = "Malware is malicious software designed to harm or exploit systems. Keep your OS and antivirus updated, and avoid downloading files from untrusted sources."
    elif 'hello' in message or 'hi' in message:
        response = "Hello! How can I assist you with your cybersecurity needs today?"
        
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
