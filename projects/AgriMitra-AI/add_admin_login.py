import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

admin_routes = """
@app.route("/admin/login")
def admin_login_page():
    return render_template("admin_login.html")

@app.route("/api/admin/login", methods=["POST"])
def api_admin_login():
    data = request.get_json(silent=True) or {}
    userid = str(data.get("userid", "")).strip()
    password = str(data.get("password", ""))
    
    if userid != 'admin':
        return jsonify({"success": False, "message": "Invalid admin credentials."}), 401
        
    user = User.query.filter_by(userid=userid).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"success": False, "message": "Invalid admin credentials."}), 401
        
    session["user_id"] = user.id
    session["language"] = user.language
    return jsonify({"success": True})

@app.route("/admin")
@login_required
def admin_dashboard():
    user = get_logged_in_user()
    if user.userid != "admin":
        return redirect(url_for("admin_login_page"))
    return render_template("admin.html")
"""

# Replace the existing admin_dashboard route
content = re.sub(r'@app\.route\("/admin"\)\s+@login_required\s+def admin_dashboard\(\):[\s\S]*?return render_template\("admin\.html"\)', admin_routes.strip(), content)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Added admin login routes.")
