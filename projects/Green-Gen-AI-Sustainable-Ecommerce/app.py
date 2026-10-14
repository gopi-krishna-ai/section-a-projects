import os
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from models import db, User, Product, Interaction, Order, OrderItem, RecyclingRequest
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'green_gen_ai_super_secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///green_gen.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db.init_app(app)

# Helper to get current user
def get_current_user():
    user_id = session.get('user_id')
    if user_id:
        return User.query.get(user_id)
    return None

def log_interaction(user_id, product_id, event_type):
    interaction = Interaction(user_id=user_id, product_id=product_id, event_type=event_type)
    db.session.add(interaction)
    db.session.commit()

import json

def get_category_images():
    try:
        with open('data/categories.json', 'r') as f:
            return json.load(f)
    except:
        return {}

def save_category_images(data):
    with open('data/categories.json', 'w') as f:
        json.dump(data, f)

from werkzeug.security import check_password_hash, generate_password_hash

@app.route('/')
def landing_page():
    return render_template('landing.html', user=get_current_user())

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    error = None
    if request.method == 'POST':
        username = request.form.get('username', '').strip().lower()
        password = request.form.get('password', '').strip()
        user = User.query.filter_by(username=username).first()
        if user and user.password_hash and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            return redirect(url_for('home'))
        else:
            error = "Invalid username or password"
            
    return render_template('login_page.html', user=get_current_user(), error=error)

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    error = None
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        username = request.form.get('username', '').strip().lower()
        password = request.form.get('password', '')
        
        # Check if user exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            error = "Username already taken."
        else:
            new_user = User(
                username=username, 
                name=name, 
                password_hash=generate_password_hash(password),
                persona="New User"
            )
            db.session.add(new_user)
            db.session.commit()
            
            session['user_id'] = new_user.id
            return redirect(url_for('home'))
            
    return render_template('register.html', user=get_current_user(), error=error)

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login_page():
    error = None
    if request.method == 'POST':
        username = request.form.get('username', '').strip().lower()
        password = request.form.get('password', '').strip()
        user = User.query.filter_by(username=username).first()
        if user and getattr(user, 'is_admin', False) and user.password_hash and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            return redirect(url_for('admin_dashboard'))
        else:
            error = "Invalid admin credentials"
            
    return render_template('admin_login.html', user=get_current_user(), error=error)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('landing_page'))

@app.route('/store')
def home():
    user = get_current_user()
    if not user:
        return redirect(url_for('login_page'))
    
    # Featured / Highest Eco Score products
    top_eco_products = Product.query.order_by(Product.eco_score.desc()).limit(8).all()
    categories = db.session.query(Product.category).distinct().all()
    categories = [c[0] for c in categories if c[0]]
    
    return render_template('home.html', user=user, top_eco_products=top_eco_products, categories=categories)


@app.route('/refurbished')
def refurbished():
    user = get_current_user()
    
    # Get a random sample of products to act as refurbished/recycled
    all_products = Product.query.all()
    import random
    refurbished_products = random.sample(all_products, min(12, len(all_products))) if all_products else []
    
    # Assign a mock 'recycled_by' property to each for display
    mock_names = ['Alice', 'Bob', 'Carol', 'David', 'Emma', 'Frank', 'Grace', 'Henry']
    for p in refurbished_products:
        p.recycled_by = random.choice(mock_names)
        # Reduce price by 40% for refurbished
        p.refurbished_price = int(p.price_inr * 0.6)
        
    return render_template('refurbished.html', products=refurbished_products, user=user)

@app.route('/products')
def product_catalog():
    user = get_current_user()
    category = request.args.get('category')
    search = request.args.get('search')
    min_eco = request.args.get('min_eco', type=int)

    query = Product.query

    if category:
        query = query.filter(Product.category == category)
    if search:
        query = query.filter(Product.name.ilike(f'%{search}%'))
    if min_eco:
        query = query.filter(Product.eco_score >= min_eco)

    # Randomly shuffle results so different categories are shown first
    query = query.order_by(db.func.random())
    
    products = query.limit(50).all()
    
    # Get categories for the visual filter
    categories = db.session.query(Product.category).distinct().all()
    categories = [c[0] for c in categories if c[0]]
    
    cat_images = get_category_images()
    
    return render_template('products.html', products=products, user=user, categories=categories, cat_images=cat_images)


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

@app.route('/product/<string:product_id>')
def product_details(product_id):
    user = get_current_user()
    product = Product.query.get_or_404(product_id)
    
    # Log view
    if user:
        log_interaction(user.id, product.id, 'VIEW')
        
    return render_template('product_details.html', product=product, user=user)

@app.route('/customize/<string:product_id>')
def customize(product_id):
    user = get_current_user()
    product = Product.query.get_or_404(product_id)
    return render_template('customize.html', product=product, user=user)

@app.route('/cart/add/<string:product_id>', methods=['POST'])
def add_to_cart(product_id):
    user = get_current_user()
    if 'cart' not in session:
        session['cart'] = {}
    
    cart = session['cart']
    cart[product_id] = cart.get(product_id, 0) + 1
    session.modified = True
    
    if user:
        log_interaction(user.id, product_id, 'CART')
        
    return jsonify({"success": True, "cart_count": sum(cart.values())})

@app.route('/api/cart/add_custom', methods=['POST'])
def add_custom_to_cart():
    user = get_current_user()
    data = request.json
    product_id = data.get('product_id')
    color = data.get('color', '')
    size = data.get('size', '')
    weight = data.get('weight', '')
    prompt = data.get('prompt', '')
    custom_charge = data.get('custom_charge', 0)
    
    if 'cart' not in session:
        session['cart'] = {}
        
    cart = session['cart']
    # Create a unique key for the customized product
    custom_key = f"{product_id}|{color}|{size}|{weight}|{prompt}|{custom_charge}"
    
    cart[custom_key] = cart.get(custom_key, 0) + 1
    session.modified = True
    
    if user:
        log_interaction(user.id, product_id, 'CART')
        
    return jsonify({"success": True, "cart_count": sum(cart.values())})

@app.route('/api/customize_chat', methods=['POST'])
def customize_chat():
    data = request.json
    text = data.get('message', '').lower()
    product_id = data.get('product_id')
    
    p = Product.query.get(product_id)
    if not p:
        return jsonify({"error": "Product not found"}), 404
        
    details = []
    charge = 0
    
    # Simple NLP rules for mockup
    colors = ['pink', 'blue', 'red', 'green', 'black', 'white', 'yellow', 'purple', 'orange', 'dark blue']
    found_color = None
    for c in colors:
        if c in text:
            found_color = c.title()
            break
            
    if found_color:
        details.append({"label": "Color", "val": found_color, "price": 50})
        charge += 50
        
    if 'floral' in text or 'pattern' in text:
        details.append({"label": "Pattern", "val": "Floral Pattern", "price": 100})
        charge += 100
        
    if 'name' in text or 'print' in text or 'text' in text:
        details.append({"label": "Custom Print", "val": "Personalized Text", "price": 50})
        charge += 50
        
    # Size detection (with synonyms)
    if any(word in text for word in ['xl', 'extra large', 'huge', 'biggest']):
        details.append({"label": "Size", "val": "Extra Large (XL)", "price": 150})
        charge += 150
    elif any(word in text for word in ['large', 'bigger', 'big', 'l ']):
        details.append({"label": "Size", "val": "Large (L)", "price": 100})
        charge += 100
    elif any(word in text for word in ['medium', 'regular', 'm ']):
        details.append({"label": "Size", "val": "Medium (M)", "price": 0})
    elif any(word in text for word in ['small', 'smaller', 'tiny', 's ']):
        details.append({"label": "Size", "val": "Small (S)", "price": 0})
        
    # Validation: If no specific keywords were found, check if it seems like a valid vague request 
    # (e.g. contains words like 'want', 'make', 'add', 'custom')
    valid_vague_words = ['make', 'add', 'custom', 'design', 'style', 'change', 'size', 'want']
    if not details:
        is_valid_vague = any(word in text for word in valid_vague_words)
        
        if not is_valid_vague:
            # Reject irrelevant queries
            response_html = f"""
            <div class="flex flex-col gap-3 w-full text-gray-800">
                <p class="text-base text-red-600 font-medium">Sorry, I didn't understand that request.</p>
                <p class="text-sm text-gray-600">I am a customization assistant for Green Gen AI. I can help you change colors, add patterns, or print text on this product.</p>
                <p class="text-sm text-gray-600">Please try asking something like: <em>"Make it blue"</em> or <em>"Add a floral pattern"</em>.</p>
            </div>
            """
            return jsonify({"html": response_html})
            
        details.append({"label": "Custom Request", "val": "Review requested", "price": 50})
        charge += 50
        
    response_html = f"""
    <div class="flex flex-col gap-3 w-full text-gray-800">
        <p class="text-base">Got it! ✨ You want <strong>{text}</strong>.</p>
        <p class="text-sm text-gray-600 mb-2">Here's the customization and price calculation:</p>
        
        <div class="bg-pink-50 rounded-xl border border-pink-200 overflow-hidden text-sm shadow-sm w-full max-w-sm">
            <div class="bg-pink-100 px-4 py-3 font-bold text-pink-900 flex items-center gap-2">
                <i class="fa-solid fa-palette text-pink-600"></i> Customization Details
            </div>
            <div class="p-4 flex flex-col gap-3">
    """
    
    for d in details:
        price_str = f"+₹{d['price']}" if d['price'] > 0 else "(No extra charge)"
        response_html += f"""
                <div class="flex justify-between items-center text-gray-700">
                    <span class="text-gray-500 w-1/3">{d['label']}</span>
                    <span class="font-medium flex-1 text-left">{d['val']}</span>
                    <span class="text-green-600 text-right text-xs whitespace-nowrap">{price_str}</span>
                </div>
        """
        
    final_price = p.price_inr + charge
        
    response_html += f"""
            </div>
            <div class="bg-purple-100 px-4 py-3 font-bold text-purple-900 flex items-center gap-2 border-t border-purple-200">
                <i class="fa-solid fa-indian-rupee-sign text-purple-600"></i> Price Summary
            </div>
            <div class="p-4 flex flex-col gap-2 text-gray-700">
                <div class="flex justify-between items-center">
                    <span class="text-gray-500">Base Product Price</span>
                    <span class="font-medium">₹{p.price_inr:.2f}</span>
                </div>
                <div class="flex justify-between items-center border-b border-gray-200 pb-3 mb-1">
                    <span class="text-gray-500">Customization Charge</span>
                    <span class="font-medium">+₹{charge:.2f}</span>
                </div>
                <div class="flex justify-between items-center font-bold text-emerald-800 text-base bg-emerald-100 px-3 py-2 rounded-lg mt-1">
                    <span>Final Price</span>
                    <span>₹{final_price:.2f}</span>
                </div>
            </div>
        </div>
        
        <div class="mt-2 flex flex-col gap-3">
            <p class="text-sm font-medium text-purple-900">Would you like to add this customized product to your cart?</p>
            <div class="flex flex-col sm:flex-row gap-3">
                <button onclick="addCustomToCart('{product_id}', '{charge}', '{text}')" class="bg-emerald-600 hover:bg-emerald-700 text-white px-5 py-2.5 rounded-xl font-bold shadow-sm transition-colors flex items-center justify-center gap-2 flex-1">
                    <i class="fa-solid fa-cart-shopping"></i> Confirm & Add to Cart
                </button>
                <button onclick="resetChat()" class="bg-white hover:bg-gray-50 text-gray-700 border border-gray-300 px-5 py-2.5 rounded-xl font-bold shadow-sm transition-colors flex items-center justify-center gap-2 flex-1">
                    <i class="fa-solid fa-pen"></i> Change Customization
                </button>
            </div>
        </div>
    </div>
    """
    
    return jsonify({"html": response_html})

@app.route('/api/generate_preview', methods=['POST'])
def generate_preview():
    data = request.json
    product_id = data.get('product_id')
    color_hex = data.get('color_hex', '#ffffff')
    
    p = Product.query.get(product_id)
    if not p:
        return jsonify({"success": False, "error": "Product not found"}), 404
        
    try:
        from customizer import recolor_product_with_ai
        # Generate a unique filename based on product and color
        clean_hex = color_hex.replace('#', '')
        out_name = f"{product_id}_{clean_hex}.jpg"
        
        # This uses the pre-trained U^2-Net model locally
        generated_url = recolor_product_with_ai(p.image_url, color_hex, out_name)
        
        return jsonify({"success": True, "image_url": f"{generated_url}?v={os.urandom(4).hex()}"})
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/cart')
def view_cart():
    user = get_current_user()
    cart = session.get('cart', {})
    cart_items = []
    total_price = 0
    total_eco = 0
    count = 0
    
    for key, qty in cart.items():
        parts = key.split('|')
        pid = parts[0]
        p = Product.query.get(pid)
        if p:
            is_custom = len(parts) > 1
            custom_data = None
            price = p.price_inr
            img = p.image_url
            if is_custom:
                color = parts[1] if len(parts) > 1 else ''
                size = parts[2] if len(parts) > 2 else ''
                weight = parts[3] if len(parts) > 3 else ''
                prompt = parts[4] if len(parts) > 4 else ''
                custom_charge = float(parts[5]) if len(parts) > 5 else (p.price_inr * 0.15)
                
                custom_data = {'color': color, 'size': size, 'weight': weight, 'prompt': prompt}
                price = p.price_inr + custom_charge
                img = f"/static/images/customized/{pid}_{color.replace('#', '')}.jpg" if color and color.startswith('#') else p.image_url
                
            cart_items.append({
                'product': p, 
                'quantity': qty, 
                'is_custom': is_custom, 
                'custom_data': custom_data,
                'final_price': price,
                'img': img
            })
            total_price += price * qty
            total_eco += p.eco_score * qty
            count += qty
            
    avg_eco = total_eco / count if count > 0 else 0
    
    return render_template('cart.html', cart_items=cart_items, total_price=total_price, avg_eco=avg_eco, user=user)

@app.route('/checkout', methods=['POST'])
def checkout():
    user = get_current_user()
    cart = session.get('cart', {})
    if not cart or not user:
        return redirect(url_for('home'))
        
    total_price = 0
    total_eco = 0
    count = 0
    
    order = Order(user_id=user.id, total_price=0, avg_eco_score=0)
    db.session.add(order)
    db.session.flush() # get order.id
    
    for pid, qty in cart.items():
        p = Product.query.get(pid)
        if p:
            total_price += p.price_inr * qty
            total_eco += p.eco_score * qty
            count += qty
            
            item = OrderItem(order_id=order.id, product_id=p.id, quantity=qty, price_at_purchase=p.price_inr)
            db.session.add(item)
            log_interaction(user.id, p.id, 'PURCHASE')
            
    order.total_price = total_price
    order.avg_eco_score = total_eco / count if count > 0 else 0
    
    user.green_points += int(order.avg_eco_score) # Reward for shopping sustainable
    
    db.session.commit()
    session['cart'] = {}
    
    return render_template('order_confirmation.html', order=order, user=user)

@app.route('/profile')
def profile():
    user = get_current_user()
    if not user:
        return redirect(url_for('login_page'))
    orders = Order.query.filter_by(user_id=user.id).order_by(Order.timestamp.desc()).all()
    recycling = RecyclingRequest.query.filter_by(user_id=user.id).all()
    
    return render_template('profile.html', user=user, orders=orders, recycling=recycling)

@app.route('/recycle', methods=['GET', 'POST'])
def recycle():
    user = get_current_user()
    if not user:
        return redirect(url_for('login_page'))
    if request.method == 'POST':
        product_id = request.form.get('product_id')
        condition = request.form.get('condition')
        reason = request.form.get('reason')
        
        req = RecyclingRequest(
            user_id=user.id, 
            product_id=product_id,
            condition=condition,
            reason=reason,
            status='Pending Verification'
        )
        db.session.add(req)
        db.session.commit()
        return redirect(url_for('profile'))
        
    # Get products the user has ordered
    purchased_product_ids = [item.product_id for order in user.orders for item in order.items]
    eligible_products = Product.query.filter(Product.id.in_(purchased_product_ids)).all()
    
    return render_template('recycle.html', user=user, products=eligible_products)

@app.route('/admin/verify_recycle/<int:req_id>', methods=['POST'])
def verify_recycle(req_id):
    req = RecyclingRequest.query.get_or_404(req_id)
    req.status = 'Verified'
    req.user.green_points += 250
    db.session.commit()
    return redirect(url_for('profile'))

@app.route('/recommendations')
def recommendations():
    user = get_current_user()
    if not user:
        return redirect(url_for('login_page'))
    # We will load recommendations from a JSON file generated by our ML script
    # For now, fallback to top eco products if ML not run
    import json
    try:
        with open('data/recommendations.json', 'r') as f:
            recs = json.load(f)
            user_recs = recs.get(str(user.id), [])
            # user_recs is a list of dicts: {"product_id": "...", "reason": "..."}
            
            recommended_products = []
            for r in user_recs:
                p = Product.query.get(r['product_id'])
                if p:
                    recommended_products.append({'product': p, 'reason': r['reason']})
    except Exception as e:
        print("ML recs not found, fallback", e)
        # Fallback
        fallback = Product.query.filter(Product.eco_score > 80).limit(8).all()
        recommended_products = [{'product': p, 'reason': "High Eco Score."} for p in fallback]
        
    return render_template('recommendations.html', user=user, recommendations=recommended_products)

@app.route('/architecture')
def architecture():
    return render_template('architecture.html', user=get_current_user())

@app.route('/admin/dashboard')
def admin_dashboard():
    user = get_current_user()
    if not user or not user.is_admin:
        return redirect(url_for('login_page'))
    products = Product.query.order_by(Product.id.desc()).all()
    return render_template('admin_dashboard.html', user=user, products=products)

@app.route('/admin/product/add', methods=['GET', 'POST'])
def admin_add_product():
    user = get_current_user()
    if not user or not user.is_admin:
        return redirect(url_for('login_page'))
        
    if request.method == 'POST':
        name = request.form.get('name')
        category = request.form.get('category')
        price_inr = request.form.get('price_inr', type=float)
        eco_score = request.form.get('eco_score', type=float)
        description = request.form.get('description')
        
        # New Sustainability Details
        material_type = request.form.get('material_type', 'Eco-Friendly Material')
        recycled_content_pct = request.form.get('recycled_content_pct', type=float) or 50.0
        recyclability_pct = request.form.get('recyclability_pct', type=float) or 50.0
        manufacturing_process = request.form.get('manufacturing_process', 'Standard')
        packaging_type = request.form.get('packaging_type', 'Recycled Box')
        packaging_recyclable_pct = request.form.get('packaging_recyclable_pct', type=float) or 80.0
        carbon_footprint_kg = request.form.get('carbon_footprint_kg', type=float) or 2.0
        
        image = request.files.get('image')
        image_url = ''
        if image and image.filename:
            filename = secure_filename(image.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(filepath)
            image_url = url_for('static', filename=f"uploads/{filename}")
            
        new_prod_id = f"PROD_{int(datetime.utcnow().timestamp())}"
        
        p = Product(
            id=new_prod_id,
            name=name,
            category=category,
            price_inr=price_inr,
            eco_score=eco_score,
            description=description,
            image_url=image_url,
            material_type=material_type,
            recycled_content_pct=recycled_content_pct,
            recyclability_pct=recyclability_pct,
            manufacturing_process=manufacturing_process,
            packaging_type=packaging_type,
            packaging_recyclable_pct=packaging_recyclable_pct,
            carbon_footprint_kg=carbon_footprint_kg,
            eco_label="New Eco Product"
        )
        db.session.add(p)
        db.session.commit()
        
        # Trigger ML pipeline in background so the new product is indexed
        import threading
        import subprocess
        threading.Thread(target=lambda: subprocess.run(['python', 'ml/train_model.py'], cwd=os.path.dirname(os.path.abspath(__file__)))).start()
        
        return redirect(url_for('admin_dashboard'))
        
    return render_template('admin_add_product.html', user=user)

@app.route('/admin/categories', methods=['GET', 'POST'])
def admin_categories():
    user = get_current_user()
    if not user or not user.is_admin:
        return redirect(url_for('login_page'))
        
    cat_images = get_category_images()
    
    if request.method == 'POST':
        for cat in cat_images.keys():
            new_url = request.form.get(f"cat_{cat}")
            if new_url:
                cat_images[cat] = new_url
        save_category_images(cat_images)
        return redirect(url_for('admin_categories'))
        
    return render_template('admin_categories.html', user=user, cat_images=cat_images)

@app.route('/admin/product/<string:product_id>/edit_image', methods=['GET', 'POST'])
def admin_edit_image(product_id):
    user = get_current_user()
    if not user or not user.is_admin:
        return redirect(url_for('login_page'))
        
    product = Product.query.get_or_404(product_id)
    
    if request.method == 'POST':
        image_url = request.form.get('image_url')
        image_file = request.files.get('image_file')
        
        if image_file and image_file.filename:
            filename = secure_filename(image_file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image_file.save(filepath)
            product.image_url = url_for('static', filename=f"uploads/{filename}")
        elif image_url:
            product.image_url = image_url
            
        db.session.commit()
        return redirect(url_for('admin_dashboard'))
        
    return render_template('admin_edit_image.html', user=user, product=product)

# --- CHATBOT FEATURE ---
@app.route('/api/chat', methods=['POST'])
def chat_api():
    data = request.json
    query = data.get('query', '').lower()
    
    if not query:
        return jsonify({"reply": "I'm the Green Gen AI assistant! Ask me for a product to see its eco-score and price."})
        
    # Search for products matching the query
    # We do a basic search in name or category
    from models import Product
    import re
    
    # Simple extraction of keywords to search
    words = [w for w in query.split() if len(w) > 3 and w not in ["show", "find", "need", "want", "some", "product", "with", "price", "score"]]
    if not words:
        words = query.split()
        
    search_term = words[0] if words else query
    
    products = Product.query.filter(
        db.or_(
            Product.name.ilike(f"%{search_term}%"),
            Product.category.ilike(f"%{search_term}%")
        )
    ).limit(3).all()
    
    if not products:
        return jsonify({"reply": f"I couldn't find any products matching '{search_term}'. Try searching for things like 'shirt', 'laptop', or 'shoe'."})
        
    reply_html = f"<p>Here are some <strong>{search_term}</strong> options I found:</p><div style='display:flex; flex-direction:column; gap:10px; margin-top:10px;'>"
    
    for p in products:
        reply_html += f"""
        <div style="border: 1px solid #e5e7eb; border-radius: 8px; padding: 10px; background: white;">
            <p style="font-weight:bold; margin-bottom: 5px;">{p.name}</p>
            <p style="margin-bottom: 5px; font-size: 0.9em;">
                <span style="color: #059669;"><i class="fas fa-leaf"></i> Eco Score: {p.eco_score}/10</span> | 
                <span style="color: #4b5563;"><i class="fas fa-tag"></i> ₹{p.price_inr}</span>
            </p>
            <a href="/product/{p.id}" style="display: inline-block; background: #059669; color: white; padding: 5px 10px; border-radius: 5px; text-decoration: none; font-size: 0.85em;">View Product</a>
        </div>
        """
    reply_html += "</div>"
    
    return jsonify({"reply": reply_html})

if __name__ == '__main__':
    if not os.path.exists('green_gen.db'):
        print("Please run 'python setup_db.py' first.")
    app.run(debug=True, port=5001)
