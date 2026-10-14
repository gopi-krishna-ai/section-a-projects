import os
import re

app_path = 'app.py'
with open(app_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Make sure we add session and redirect to imports
if 'from flask import Flask, render_template, request, jsonify, redirect, url_session, session, flash' not in content:
    content = content.replace(
        'from flask import Flask, render_template, request, jsonify',
        'from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash'
    )
    content = content.replace('import json\n', '')
    content = content.replace('import joblib', 'import joblib\nimport json\nimport os')

# Setup secret key
if "app.secret_key =" not in content:
    content = content.replace('app = Flask(__name__)', "app = Flask(__name__)\napp.secret_key = 'super_secret_resqai_key'")

# Update route mappings
old_index = '''@app.route('/')
def index():
    return render_template('index.html')'''

new_routes = '''
USER_FILE = 'data/users.json'

def load_users():
    if not os.path.exists(USER_FILE):
        return {}
    with open(USER_FILE, 'r') as f:
        return json.load(f)

def save_users(users):
    with open(USER_FILE, 'w') as f:
        json.dump(users, f)

@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        users = load_users()
        
        if email in users and users[email] == password:
            session['user'] = email
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials. Please try again.', 'danger')
            
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        users = load_users()
        
        if email in users:
            flash('Email already registered. Please login.', 'warning')
            return redirect(url_for('login'))
            
        users[email] = password
        save_users(users)
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
        
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('landing'))

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')
'''

content = content.replace(old_index, new_routes)

# Also protect /assistant
old_assistant = '''@app.route('/assistant')
def assistant():
    return render_template('assistant.html')'''

new_assistant = '''@app.route('/assistant')
def assistant():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('assistant.html')'''

content = content.replace(old_assistant, new_assistant)

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(content)

# Ensure users.json exists
if not os.path.exists('data/users.json'):
    with open('data/users.json', 'w') as f:
        f.write('{}')
