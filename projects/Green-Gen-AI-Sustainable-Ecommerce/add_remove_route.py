with open('app.py', 'r', encoding='utf-8') as f:
    app_py = f.read()

remove_route = """
@app.route('/product/remove/<string:product_id>', methods=['POST'])
def remove_product(product_id):
    user = get_current_user()
    if not user or not user.is_admin:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({"success": False, "error": "Unauthorized"}), 403
        return redirect(url_for('home'))
        
    product = Product.query.get(product_id)
    if product:
        Interaction.query.filter_by(product_id=product_id).delete()
        OrderItem.query.filter_by(product_id=product_id).delete()
        RecyclingRequest.query.filter_by(product_id=product_id).delete()
        db.session.delete(product)
        db.session.commit()
        
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({"success": True})
        
    return redirect(request.referrer or url_for('product_catalog'))
"""

if 'def remove_product' not in app_py:
    app_py = app_py.replace("@app.route('/product/<string:product_id>')", remove_route + "\n@app.route('/product/<string:product_id>')")
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(app_py)
