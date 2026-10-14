import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update Order model
order_replacement = """class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default='Pending Approval')
    delivery_address = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())"""

content = re.sub(r'class Order\(db\.Model\):[\s\S]*?created_at = db\.Column\(db\.DateTime, default=db\.func\.current_timestamp\(\)\)', order_replacement, content)

# 2. Update /api/checkout default status
content = content.replace("order = Order(user_id=user.id, total_amount=0)", "order = Order(user_id=user.id, total_amount=0, status='Pending Approval')")

# 3. Add user orders API & Route
user_orders_routes = """
@app.route("/my-orders")
@login_required
def my_orders_page():
    user = get_logged_in_user()
    return render_template("orders.html", user=user, language=current_language(user), active_page="orders")

@app.route("/api/my-orders", methods=["GET"])
@login_required
def api_my_orders():
    user = get_logged_in_user()
    orders = Order.query.filter_by(user_id=user.id).order_by(Order.created_at.desc()).all()
    res = []
    for o in orders:
        items = OrderItem.query.filter_by(order_id=o.id).all()
        items_res = []
        for i in items:
            p = Product.query.get(i.product_id)
            items_res.append({"name": p.item_name if p else "Deleted", "quantity": i.quantity, "price": i.price})
        res.append({
            "id": o.id,
            "total_amount": o.total_amount,
            "status": o.status,
            "delivery_address": o.delivery_address,
            "created_at": o.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "items": items_res
        })
    return jsonify({"success": True, "orders": res})

@app.route("/api/orders/<int:order_id>/location", methods=["POST"])
@login_required
def provide_location(order_id):
    user = get_logged_in_user()
    o = Order.query.get_or_404(order_id)
    if o.user_id != user.id:
        return jsonify({"success": False}), 403
    address = request.json.get("address")
    if not address:
        return jsonify({"success": False, "message": "Address is required"}), 400
    
    o.delivery_address = address
    o.status = "Location Provided"
    db.session.commit()
    return jsonify({"success": True})
"""
if 'def my_orders_page():' not in content:
    content = content.replace('if __name__ == "__main__":', user_orders_routes + '\nif __name__ == "__main__":')

# 4. Update /api/admin/orders to include delivery_address
content = content.replace('"status": o.status,', '"status": o.status, "delivery_address": o.delivery_address,')

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)
print("app.py updated for order flow")
