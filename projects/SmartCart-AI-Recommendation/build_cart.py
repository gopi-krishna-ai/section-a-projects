import os

def build_cart_system():
    # 1. Update backend/routes.py
    with open('backend/routes.py', 'r', encoding='utf-8') as f:
        routes_code = f.read()

    # We need to add a context processor for cart_count
    context_processor = """
    @app.context_processor
    def inject_cart_count():
        cart = session.get('cart', {})
        count = sum(cart.values())
        return dict(cart_count=count)
    """
    
    if "def inject_cart_count():" not in routes_code:
        # insert after @app.route('/')
        routes_code = routes_code.replace(
            "@app.route('/')", 
            context_processor + "\n    @app.route('/')"
        )
        
    # Replace the old mock cart routes with a real session-based cart
    old_cart_routes = """    @app.route('/add_to_cart/<int:product_id>', methods=['POST'])
    def add_to_cart(product_id):
        flash("Product added to cart! (Demo Mode)", "success")
        return redirect(url_for('cart'))

    @app.route('/cart')
    def cart():
        return render_template('cart.html')"""
        
    new_cart_routes = """    @app.route('/add_to_cart/<int:product_id>', methods=['POST'])
    def add_to_cart(product_id):
        quantity = int(request.form.get('quantity', 1))
        
        if 'cart' not in session:
            session['cart'] = {}
            
        cart = session['cart']
        prod_id_str = str(product_id)
        
        if prod_id_str in cart:
            cart[prod_id_str] += quantity
        else:
            cart[prod_id_str] = quantity
            
        session.modified = True
        flash("Product added to cart!", "success")
        return redirect(url_for('cart'))
        
    @app.route('/remove_from_cart/<int:product_id>', methods=['POST'])
    def remove_from_cart(product_id):
        if 'cart' in session:
            prod_id_str = str(product_id)
            if prod_id_str in session['cart']:
                session['cart'].pop(prod_id_str)
                session.modified = True
                flash("Product removed from cart.", "info")
        return redirect(url_for('cart'))

    @app.route('/cart')
    def cart():
        cart_data = session.get('cart', {})
        cart_items = []
        total_price = 0.0
        
        for prod_id, quantity in cart_data.items():
            product = Product.query.get(int(prod_id))
            if product:
                subtotal = product.price * quantity
                total_price += subtotal
                cart_items.append({
                    'product': product,
                    'quantity': quantity,
                    'subtotal': subtotal
                })
                
        return render_template('cart.html', cart_items=cart_items, total_price=total_price)
        
    @app.route('/checkout', methods=['POST'])
    def checkout():
        if 'customer_id' not in session:
            flash("Please login to checkout.", "warning")
            return redirect(url_for('login'))
            
        if not session.get('cart'):
            flash("Your cart is empty.", "warning")
            return redirect(url_for('cart'))
            
        # Clear cart
        session['cart'] = {}
        session.modified = True
        flash("Order placed successfully! Thank you for shopping with SmartCart.", "success")
        return redirect(url_for('orders'))"""
        
    # If old mock is there, replace it
    if "def add_to_cart(product_id):" in routes_code:
        # Regex replacement because exact spacing might differ
        import re
        routes_code = re.sub(r"@app\.route\('/add_to_cart/<int:product_id>'.*?return render_template\('cart\.html'\)", new_cart_routes, routes_code, flags=re.DOTALL)
    
    with open('backend/routes.py', 'w', encoding='utf-8') as f:
        f.write(routes_code)
        
    print("Routes updated with real cart logic!")

    # 2. Create templates/cart.html
    cart_html = """{% extends "base.html" %}
{% block content %}
<div class="row mt-4 mb-5">
    <div class="col-md-8">
        <h2 class="fw-bold mb-4"><i class="fas fa-shopping-cart text-primary"></i> Your Shopping Cart</h2>
        
        {% if cart_items %}
            <div class="card product-card border-0 p-4">
                <div class="table-responsive">
                    <table class="table align-middle">
                        <thead class="table-light">
                            <tr>
                                <th>Product</th>
                                <th>Price</th>
                                <th>Quantity</th>
                                <th>Subtotal</th>
                                <th>Action</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for item in cart_items %}
                            <tr>
                                <td>
                                    <div class="d-flex align-items-center">
                                        <img src="{% if item.product.image_url and item.product.image_url.startswith('http') %}{{ item.product.image_url }}{% else %}{{ url_for('static', filename=item.product.image_url) }}{% endif %}" class="rounded shadow-sm me-3" style="width: 60px; height: 60px; object-fit: cover;">
                                        <div>
                                            <h6 class="mb-0 fw-bold">{{ item.product.name }}</h6>
                                            <small class="text-muted">{{ item.product.category.name }}</small>
                                        </div>
                                    </div>
                                </td>
                                <td>${{ "%.2f"|format(item.product.price) }}</td>
                                <td class="fw-bold">{{ item.quantity }}</td>
                                <td class="fw-bold text-success">${{ "%.2f"|format(item.subtotal) }}</td>
                                <td>
                                    <form action="{{ url_for('remove_from_cart', product_id=item.product.id) }}" method="POST">
                                        <button type="submit" class="btn btn-sm btn-outline-danger rounded-circle" title="Remove"><i class="fas fa-trash"></i></button>
                                    </form>
                                </td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>
        {% else %}
            <div class="card product-card border-0 p-5 text-center">
                <i class="fas fa-shopping-basket fa-4x text-muted opacity-50 mb-3"></i>
                <h4 class="fw-bold">Your cart is empty</h4>
                <p class="text-muted">Looks like you haven't added anything to your cart yet.</p>
                <a href="{{ url_for('shop') }}" class="btn btn-primary rounded-pill px-4 mt-2">Start Shopping</a>
            </div>
        {% endif %}
    </div>
    
    <div class="col-md-4">
        <div class="card product-card border-0 p-4" style="background: linear-gradient(145deg, #ffffff, #f9fafb);">
            <h4 class="fw-bold mb-4">Order Summary</h4>
            
            <div class="d-flex justify-content-between mb-3">
                <span class="text-muted">Subtotal</span>
                <span class="fw-bold">${{ "%.2f"|format(total_price) }}</span>
            </div>
            <div class="d-flex justify-content-between mb-3">
                <span class="text-muted">Shipping</span>
                <span class="fw-bold text-success">Free</span>
            </div>
            <hr>
            <div class="d-flex justify-content-between mb-4">
                <span class="fw-bold fs-5">Total</span>
                <span class="fw-bold fs-4 text-primary">${{ "%.2f"|format(total_price) }}</span>
            </div>
            
            <form action="{{ url_for('checkout') }}" method="POST">
                <button type="submit" class="btn btn-primary w-100 py-3 rounded-pill fw-bold fs-6 shadow-sm" {% if not cart_items %}disabled{% endif %}>
                    Proceed to Checkout <i class="fas fa-arrow-right ms-2"></i>
                </button>
            </form>
            <div class="text-center mt-3">
                <small class="text-muted"><i class="fas fa-lock me-1"></i> Secure Encrypted Checkout</small>
            </div>
        </div>
    </div>
</div>
{% endblock %}"""
    with open('templates/cart.html', 'w', encoding='utf-8') as f:
        f.write(cart_html)
        
    print("cart.html created!")

if __name__ == '__main__':
    build_cart_system()
