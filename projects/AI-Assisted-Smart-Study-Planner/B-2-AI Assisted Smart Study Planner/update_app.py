import re

with open('app.py', 'r') as f:
    app_py = f.read()

# Add session to imports
app_py = app_py.replace('from flask import Flask, jsonify, render_template, request', 
                        'from flask import Flask, jsonify, render_template, request, session, redirect, url_for')
app_py = app_py.replace('from utils.storage import load_store, save_store',
                        'from utils.storage import load_store, save_store, register_user, verify_user')

# Add secret key
app_py = app_py.replace('app = Flask(__name__)', 'app = Flask(__name__)\nimport secrets\napp.secret_key = secrets.token_hex(16)')

# Update / route (login page)
new_login_route = '''@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        action = request.form.get("action")
        username = request.form.get("username")
        password = request.form.get("password")
        if not username or not password:
            return render_template("login.html", error="Username and password required")
        
        if action == "register":
            if register_user(username, password):
                session["username"] = username
                return redirect(url_for("index"))
            else:
                return render_template("login.html", error="Username already exists")
        elif action == "login":
            if verify_user(username, password):
                session["username"] = username
                return redirect(url_for("index"))
            else:
                return render_template("login.html", error="Invalid credentials")
    
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))
'''
app_py = re.sub(r'@app\.route\("/"\)\s*def login\(\):\s*return render_template\("login\.html"\)', new_login_route, app_py)

# Update other routes to check session and use username
def add_session_check(match):
    func_def = match.group(0)
    return f'''{func_def}
    if "username" not in session:
        return redirect(url_for("login"))
    username = session["username"]'''

def add_session_check_api(match):
    func_def = match.group(0)
    return f'''{func_def}
    if "username" not in session:
        return jsonify({{"error": "Unauthorized"}}), 401
    username = session["username"]'''

# Add check to /app and /tutor
app_py = re.sub(r'@app\.route\("/app"\)\s*def index\(\):', add_session_check, app_py)
app_py = re.sub(r'@app\.route\("/tutor"\)\s*def tutor_page\(\):', add_session_check, app_py)

# Add check to APIs
for route in ['chat_api', 'view', 'add_subject', 'delete_subject', 'upload_syllabus', 'session_complete', 'session_missed', 'update_settings']:
    app_py = re.sub(rf'def {route}\([^)]*\):', add_session_check_api, app_py)

# Replace load_store() with load_store(username)
app_py = app_py.replace('load_store()', 'load_store(username)')
# Replace save_store(store) with save_store(store, username)
app_py = app_py.replace('save_store(store)', 'save_store(store, username)')

with open('app.py', 'w') as f:
    f.write(app_py)
print("Updated app.py")
