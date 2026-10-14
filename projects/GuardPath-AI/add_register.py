import os
import re

base_dir = r'C:\Users\krish\OneDrive\Desktop\section a\01_GuardPath_AI_Updated\B-1-GuardPath AI'
app_path = os.path.join(base_dir, 'app.py')

with open(app_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace hardcoded USERS dict with JSON loading
old_users_code = '''# Mock Data for Users and History
USERS = {
    'admin': {'password': 'admin', 'role': 'admin', 'name': 'System Admin'},
    'passenger1': {'password': 'pass1', 'role': 'passenger', 'name': 'Alice', 'contacts': ['+1234567890']},
    'passenger2': {'password': 'pass2', 'role': 'passenger', 'name': 'Bob', 'contacts': ['+0987654321']}
}'''

new_users_code = '''import json

USERS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "users.json")

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=4)'''

content = content.replace(old_users_code, new_users_code)

# We need to replace all instances of USERS with load_users()
content = content.replace("username in USERS and USERS[username]", "username in load_users() and load_users()[username]")
content = content.replace("contacts = USERS.get", "contacts = load_users().get")

# Add register route
register_route = '''@app.route("/register", methods=["GET", "POST"])
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

'''

content = content.replace('@app.route("/logout")', register_route + '@app.route("/logout")')

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(content)

