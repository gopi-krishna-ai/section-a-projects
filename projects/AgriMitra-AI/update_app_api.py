import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Update /api/products GET
api_products = """@app.route("/api/products", methods=["GET"])
def get_products():
    products = Product.query.all()
    res = []
    for p in products:
        res.append({
            "id": p.id,
            "item_type": p.item_type,
            "item_name": p.item_name,
            "seller": p.seller,
            "description": p.description,
            "price": p.price,
            "image_url": p.image_url,
            "stock": p.stock,
            "discount": p.discount
        })
    return jsonify(res)"""

content = re.sub(r'@app\.route\("/api/products", methods=\["GET"\]\)[\s\S]*?return jsonify\(res\)', api_products, content)

# Update /api/admin/product POST
admin_product_post = """@app.route("/api/admin/product", methods=["POST"])
@login_required
def add_product():
    user = get_logged_in_user()
    if user.userid != "admin@agrimitra":
        return jsonify({"success": False, "message": "Access Denied"}), 403
    try:
        item_type = request.form.get("item_type")
        item_name = request.form.get("item_name")
        seller = request.form.get("seller")
        description = request.form.get("description")
        price = float(request.form.get("price"))
        stock = int(request.form.get("stock", 100))
        discount = int(request.form.get("discount", 0))
        
        file = request.files.get("image")
        image_url = ""
        if file and file.filename:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            image_url = f"/static/uploads/{filename}"
        else:
            image_url = request.form.get("image_url", "")

        product = Product(
            item_type=item_type,
            item_name=item_name,
            seller=seller,
            description=description,
            price=price,
            image_url=image_url,
            stock=stock,
            discount=discount
        )
        db.session.add(product)
        db.session.commit()
        return jsonify({"success": True, "message": "Product added successfully!"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400"""

content = re.sub(r'@app\.route\("/api/admin/product", methods=\["POST"\]\)[\s\S]*?return jsonify\(\{"success": False, "message": str\(e\)\}\), 400', admin_product_post, content)

# Add new admin endpoints
new_endpoints = """
@app.route("/api/admin/product/<int:product_id>", methods=["DELETE"])
@login_required
def delete_product(product_id):
    if get_logged_in_user().userid != "admin@agrimitra": return jsonify({"success": False}), 403
    p = Product.query.get_or_404(product_id)
    db.session.delete(p)
    db.session.commit()
    return jsonify({"success": True})

@app.route("/api/admin/product/<int:product_id>", methods=["PUT"])
@login_required
def update_product(product_id):
    if get_logged_in_user().userid != "admin@agrimitra": return jsonify({"success": False}), 403
    p = Product.query.get_or_404(product_id)
    data = request.get_json(silent=True) or {}
    if 'price' in data: p.price = float(data['price'])
    if 'stock' in data: p.stock = int(data['stock'])
    if 'discount' in data: p.discount = int(data['discount'])
    if 'description' in data: p.description = data['description']
    db.session.commit()
    return jsonify({"success": True})

@app.route("/api/admin/orders", methods=["GET"])
@login_required
def get_orders():
    if get_logged_in_user().userid != "admin@agrimitra": return jsonify({"success": False}), 403
    orders = Order.query.order_by(Order.created_at.desc()).all()
    res = []
    for o in orders:
        user = User.query.get(o.user_id)
        items = OrderItem.query.filter_by(order_id=o.id).all()
        items_res = []
        for i in items:
            p = Product.query.get(i.product_id)
            items_res.append({"product_name": p.item_name if p else "Deleted", "quantity": i.quantity, "price": i.price})
        res.append({
            "id": o.id,
            "user": user.fullname if user else "Unknown",
            "email": user.email if user else "",
            "total_amount": o.total_amount,
            "status": o.status,
            "created_at": o.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "items": items_res
        })
    return jsonify({"success": True, "orders": res})

@app.route("/api/admin/orders/<int:order_id>/status", methods=["POST"])
@login_required
def update_order_status(order_id):
    if get_logged_in_user().userid != "admin@agrimitra": return jsonify({"success": False}), 403
    o = Order.query.get_or_404(order_id)
    o.status = request.json.get("status", o.status)
    db.session.commit()
    return jsonify({"success": True})

@app.route("/api/admin/users", methods=["GET"])
@login_required
def get_users():
    if get_logged_in_user().userid != "admin@agrimitra": return jsonify({"success": False}), 403
    users = User.query.all()
    res = [{"id": u.id, "fullname": u.fullname, "userid": u.userid, "email": u.email, "phone": u.phone} for u in users]
    return jsonify({"success": True, "users": res})

@app.route("/api/checkout", methods=["POST"])
@login_required
def checkout():
    user = get_logged_in_user()
    data = request.get_json(silent=True) or {}
    cart = data.get("cart", [])
    if not cart: return jsonify({"success": False, "message": "Cart is empty"}), 400
    
    total = 0
    order = Order(user_id=user.id, total_amount=0)
    db.session.add(order)
    db.session.flush() # get ID
    
    for item in cart:
        # Expected item: {product_id, quantity, price}
        p = Product.query.get(item.get("product_id"))
        if p:
            qty = float(item.get("quantity", 1))
            if p.stock < qty: return jsonify({"success": False, "message": f"Not enough stock for {p.item_name}"}), 400
            p.stock -= qty
            price = float(item.get("price", p.price))
            total += price * qty
            oi = OrderItem(order_id=order.id, product_id=p.id, quantity=qty, price=price)
            db.session.add(oi)
    
    order.total_amount = total
    db.session.commit()
    return jsonify({"success": True, "message": "Order placed successfully!"})
"""

if 'def delete_product(product_id):' not in content:
    content = content.replace('if __name__ == "__main__":', new_endpoints + '\nif __name__ == "__main__":')

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated backend API routes in app.py")
