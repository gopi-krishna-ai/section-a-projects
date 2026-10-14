import re

with open('app.py', 'r', encoding='utf-8') as f:
    app_content = f.read()

# Update /api/checkout
old_checkout = """@app.route("/api/checkout", methods=["POST"])
@login_required
def checkout():
    user = get_logged_in_user()
    data = request.get_json(silent=True) or {}
    cart = data.get("cart", [])
    if not cart: return jsonify({"success": False, "message": "Cart is empty"}), 400
    
    total = 0
    order = Order(user_id=user.id, total_amount=0, status='Pending Approval')"""

new_checkout = """@app.route("/api/checkout", methods=["POST"])
@login_required
def checkout():
    user = get_logged_in_user()
    data = request.get_json(silent=True) or {}
    cart = data.get("cart", [])
    address = data.get("address", "")
    if not cart: return jsonify({"success": False, "message": "Cart is empty"}), 400
    
    total = 0
    order = Order(user_id=user.id, total_amount=0, status='Pending', delivery_address=address)"""

app_content = app_content.replace(old_checkout, new_checkout)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(app_content)
print("Updated app.py checkout logic.")
