import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Add protection to admin routes
admin_protect = """@app.route("/admin")
@login_required
def admin_dashboard():
    user = get_logged_in_user()
    if user.userid != 'admin':
        return "Access Denied: You must be an admin to view this page.", 403
    return render_template("admin.html")

@app.route("/api/admin/product", methods=["POST"])
@login_required
def add_product():
    user = get_logged_in_user()
    if user.userid != 'admin':
        return jsonify({"success": False, "message": "Access Denied"}), 403"""

# Replace existing def admin_dashboard and add_product definitions
content = re.sub(r'@app\.route\("/admin"\)\s+def admin_dashboard\(\):[\s\S]*?return render_template\("admin\.html"\)', 
                 '@app.route("/admin")\n@login_required\ndef admin_dashboard():\n    user = get_logged_in_user()\n    if user.userid != "admin":\n        return "Access Denied: You must be an admin to view this page.", 403\n    return render_template("admin.html")', content)

content = re.sub(r'@app\.route\("/api/admin/product", methods=\["POST"\]\)\s+def add_product\(\):',
                 '@app.route("/api/admin/product", methods=["POST"])\n@login_required\ndef add_product():\n    user = get_logged_in_user()\n    if user.userid != "admin":\n        return jsonify({"success": False, "message": "Access Denied"}), 403', content)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Admin routes secured.")
