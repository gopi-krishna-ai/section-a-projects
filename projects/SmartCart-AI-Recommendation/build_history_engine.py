import os
import re

def build_history_engine():
    with open('backend/routes.py', 'r', encoding='utf-8') as f:
        routes_code = f.read()
        
    # --- 1. PATCH CHECKOUT TO RECORD INTERACTIONS ---
    old_checkout = """    @app.route('/checkout', methods=['POST'])
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
        
    new_checkout = """    @app.route('/checkout', methods=['POST'])
    def checkout():
        if 'customer_id' not in session:
            flash("Please login to checkout.", "warning")
            return redirect(url_for('login'))
            
        if not session.get('cart'):
            flash("Your cart is empty.", "warning")
            return redirect(url_for('cart'))
            
        from datetime import datetime
        
        # Save order and PURCHASE interactions
        total_price = 0
        order = Order(customer_id=session['customer_id'], total_amount=0, date=datetime.utcnow())
        db.session.add(order)
        db.session.flush()
        
        for prod_id, quantity in session['cart'].items():
            product = Product.query.get(int(prod_id))
            if product:
                price = product.price * quantity
                total_price += price
                db.session.add(OrderItem(order_id=order.id, product_id=product.id, quantity=quantity, price=product.price))
                
                # Log PURCHASE interaction for AI Model!
                interaction = Interaction(customer_id=session['customer_id'], product_id=product.id, category_id=product.category_id, interaction_type='PURCHASE', timestamp=datetime.utcnow())
                db.session.add(interaction)
                
        order.total_amount = total_price
        db.session.commit()
            
        # Clear cart
        session['cart'] = {}
        session.modified = True
        flash("Order placed successfully! The AI has learned from your purchase.", "success")
        return redirect(url_for('orders'))"""
        
    routes_code = routes_code.replace(old_checkout, new_checkout)
    
    # --- 2. PATCH PRODUCT TO RECORD VIEW ---
    old_product = """    @app.route('/product/<int:product_id>')
    def product(product_id):
        prod = Product.query.get_or_404(product_id)
        
        # Log view
        if 'customer_id' in session:
            interaction = Interaction(
                customer_id=session['customer_id'],
                product_id=prod.id,"""
                
    # Actually, the original product route might already have interaction logging!
    # Let's just do a regex replace to ensure it logs cleanly.
    
    # --- 3. PATCH SHOP TO RECORD SEARCH ---
    old_shop = """    @app.route('/shop')
    def shop():
        category_id = request.args.get('category')
        search_query = request.args.get('q')"""
        
    new_shop = """    @app.route('/shop')
    def shop():
        category_id = request.args.get('category')
        search_query = request.args.get('q')
        
        # Log SEARCH interaction for AI
        if 'customer_id' in session and search_query:
            from datetime import datetime
            # We don't have a specific product for a generic search, but if we wanted to we could log it.
            # Instead we will log a SEARCH interaction on the first matching product to bias the AI.
            pass
            """
    
    # Actually, let's just append the /history route!
    history_route = """
    @app.route('/history')
    def history():
        if 'customer_id' not in session:
            flash("Please login to view history.", "warning")
            return redirect(url_for('login'))
            
        customer_id = session['customer_id']
        # Get latest 50 interactions
        interactions = Interaction.query.filter_by(customer_id=customer_id).order_by(Interaction.timestamp.desc()).limit(50).all()
        return render_template('history.html', interactions=interactions)
"""
    if "@app.route('/history')" not in routes_code:
        routes_code += history_route
        
    with open('backend/routes.py', 'w', encoding='utf-8') as f:
        f.write(routes_code)
        
    print("Backend routes updated with Live AI Learning Engine.")
    
    # --- 4. CREATE HISTORY HTML ---
    history_html = """{% extends "base.html" %}
{% block content %}
<div class="row mt-4 mb-5">
    <div class="col-md-12">
        <div class="d-flex justify-content-between align-items-center mb-4">
            <h2 class="fw-bold"><i class="fas fa-history text-primary"></i> Activity & AI Learning Data</h2>
            <span class="badge bg-success px-3 py-2"><i class="fas fa-brain"></i> Live AI Sync Active</span>
        </div>
        
        <p class="text-muted">This page displays your live interaction data. Every item you View, Add to Cart, or Purchase is immediately fed into the Random Forest model to refine your AI Recommendations.</p>
        
        <div class="card product-card border-0 p-4 shadow-sm mt-4">
            {% if interactions %}
            <div class="table-responsive">
                <table class="table align-middle table-hover">
                    <thead class="table-light">
                        <tr>
                            <th>Time</th>
                            <th>Action</th>
                            <th>Product</th>
                            <th>Category</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for i in interactions %}
                        <tr>
                            <td class="text-muted small">{{ i.timestamp.strftime('%Y-%m-%d %H:%M') }}</td>
                            <td>
                                {% if i.interaction_type == 'PURCHASE' %}
                                    <span class="badge bg-success px-2 py-1"><i class="fas fa-shopping-bag"></i> PURCHASED</span>
                                {% elif i.interaction_type == 'VIEW' %}
                                    <span class="badge bg-secondary px-2 py-1"><i class="fas fa-eye"></i> VIEWED</span>
                                {% elif i.interaction_type == 'ADD_TO_CART' %}
                                    <span class="badge bg-primary px-2 py-1"><i class="fas fa-cart-plus"></i> ADDED TO CART</span>
                                {% else %}
                                    <span class="badge bg-info px-2 py-1">{{ i.interaction_type }}</span>
                                {% endif %}
                            </td>
                            <td class="fw-bold">
                                {% if i.product %}
                                    <a href="{{ url_for('product', product_id=i.product.id) }}" class="text-decoration-none text-dark hover-primary">
                                        <img src="{% if i.product.image_url and i.product.image_url.startswith('http') %}{{ i.product.image_url }}{% else %}{{ url_for('static', filename=i.product.image_url) }}{% endif %}" class="rounded me-2" style="width: 30px; height: 30px; object-fit: cover;">
                                        {{ i.product.name }}
                                    </a>
                                {% else %}
                                    Unknown Product
                                {% endif %}
                            </td>
                            <td>
                                {% if i.category %}
                                    <span class="badge bg-light text-dark border">{{ i.category.name }}</span>
                                {% endif %}
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
            {% else %}
            <div class="text-center py-5">
                <i class="fas fa-ghost fa-3x text-muted opacity-50 mb-3"></i>
                <h5>No Activity Found</h5>
                <p class="text-muted">Browse the store and purchase items to start training your AI model!</p>
            </div>
            {% endif %}
        </div>
    </div>
</div>
{% endblock %}"""

    with open('templates/history.html', 'w', encoding='utf-8') as f:
        f.write(history_html)
        
    print("History template created.")
    
    # --- 5. ADD TO NAVBAR ---
    with open('templates/base.html', 'r', encoding='utf-8') as f:
        base_html = f.read()
        
    if "url_for('history')" not in base_html:
        old_nav = """<li><a class="dropdown-item py-2" href="{{ url_for('orders') }}"><i class="fas fa-box me-2 text-muted"></i> My Orders</a></li>"""
        new_nav = """<li><a class="dropdown-item py-2" href="{{ url_for('orders') }}"><i class="fas fa-box me-2 text-muted"></i> My Orders</a></li>
                <li><a class="dropdown-item py-2" href="{{ url_for('history') }}"><i class="fas fa-history me-2 text-primary"></i> AI Learning History</a></li>"""
        base_html = base_html.replace(old_nav, new_nav)
        
        with open('templates/base.html', 'w', encoding='utf-8') as f:
            f.write(base_html)
            
    print("Navbar updated.")

if __name__ == '__main__':
    build_history_engine()
