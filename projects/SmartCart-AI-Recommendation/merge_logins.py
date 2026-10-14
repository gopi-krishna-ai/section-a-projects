import os

def merge_logins():
    # 1. Update backend/routes.py
    with open('backend/routes.py', 'r', encoding='utf-8') as f:
        routes_code = f.read()
        
    old_login = """@app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            user = Customer.query.filter_by(email=email).first()
            if user and check_password_hash(user.password_hash, password):
                session['customer_id'] = user.id
                session['customer_name'] = user.name
                flash(f"Welcome back, {user.name}!", "success")
                return redirect(url_for('index'))
            else:
                flash("Invalid email or password", "danger")
        return render_template('login.html')"""
        
    new_login = """@app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            
            # --- Admin Intercept ---
            if email == 'admin@smartcart.com' and password == 'admin123':
                session['is_admin'] = True
                session['customer_name'] = "Admin"
                flash("Admin logged in successfully!", "success")
                return redirect(url_for('admin_dashboard'))
                
            # --- Standard User ---
            user = Customer.query.filter_by(email=email).first()
            if user and check_password_hash(user.password_hash, password):
                session['customer_id'] = user.id
                session['customer_name'] = user.name
                flash(f"Welcome back, {user.name}!", "success")
                return redirect(url_for('index'))
            else:
                flash("Invalid email or password", "danger")
        return render_template('login.html')"""
    
    routes_code = routes_code.replace(old_login, new_login)
    
    # 2. Remove old admin_login
    # Using python string parsing since replace_file_content is messy with large blocks
    import re
    # Remove admin_login route block
    routes_code = re.sub(r"@app\.route\('/admin/login', methods=\['GET', 'POST'\]\).*?return render_template\('admin_login\.html'\)", "", routes_code, flags=re.DOTALL)
    # Remove admin_logout route block
    routes_code = re.sub(r"@app\.route\('/admin/logout'\).*?return redirect\(url_for\('index'\)\)", "", routes_code, flags=re.DOTALL)
    
    # Fix dashboard redirect
    routes_code = routes_code.replace("redirect(url_for('admin_login'))", "redirect(url_for('login'))")
    
    with open('backend/routes.py', 'w', encoding='utf-8') as f:
        f.write(routes_code)
        
    print("Routes updated")
    
    # 3. Update base.html to remove footer link and add Admin to navbar
    with open('templates/base.html', 'r', encoding='utf-8') as f:
        base = f.read()
    
    # Replace user dropdown to add Admin Dashboard if admin
    old_dropdown = """{% if session.customer_id %}
        <li class="nav-item dropdown">
          <a class="nav-link dropdown-toggle fw-bold" href="#" id="navbarDropdown" role="button" data-bs-toggle="dropdown">
            <img src="https://ui-avatars.com/api/?name={{ session.customer_name }}&background=4F46E5&color=fff&rounded=true" alt="User" width="32" height="32" class="me-1">
            {{ session.customer_name }}
          </a>
          <ul class="dropdown-menu dropdown-menu-end border-0 shadow-lg" style="border-radius: 15px;">
            <li><a class="dropdown-item py-2" href="{{ url_for('profile') }}"><i class="fas fa-user me-2 text-muted"></i> Profile</a></li>
            <li><a class="dropdown-item py-2" href="{{ url_for('orders') }}"><i class="fas fa-box me-2 text-muted"></i> My Orders</a></li>
            <li><hr class="dropdown-divider"></li>
            <li><a class="dropdown-item py-2 text-danger" href="{{ url_for('logout') }}"><i class="fas fa-sign-out-alt me-2"></i> Logout</a></li>
          </ul>
        </li>"""
        
    new_dropdown = """{% if session.customer_id or session.is_admin %}
        <li class="nav-item dropdown">
          <a class="nav-link dropdown-toggle fw-bold" href="#" id="navbarDropdown" role="button" data-bs-toggle="dropdown">
            <img src="https://ui-avatars.com/api/?name={{ session.customer_name }}&background=4F46E5&color=fff&rounded=true" alt="User" width="32" height="32" class="me-1">
            {{ session.customer_name }}
          </a>
          <ul class="dropdown-menu dropdown-menu-end border-0 shadow-lg" style="border-radius: 15px;">
            {% if session.is_admin %}
                <li><a class="dropdown-item py-2 fw-bold text-primary" href="{{ url_for('admin_dashboard') }}"><i class="fas fa-cogs me-2"></i> Admin Dashboard</a></li>
                <li><hr class="dropdown-divider"></li>
            {% else %}
                <li><a class="dropdown-item py-2" href="{{ url_for('profile') }}"><i class="fas fa-user me-2 text-muted"></i> Profile</a></li>
                <li><a class="dropdown-item py-2" href="{{ url_for('orders') }}"><i class="fas fa-box me-2 text-muted"></i> My Orders</a></li>
                <li><hr class="dropdown-divider"></li>
            {% endif %}
            <li><a class="dropdown-item py-2 text-danger" href="{{ url_for('logout') }}"><i class="fas fa-sign-out-alt me-2"></i> Logout</a></li>
          </ul>
        </li>"""
        
    base = base.replace(old_dropdown, new_dropdown)
    
    # Remove footer admin link
    base = base.replace('<a href="{{ url_for(\'admin_login\') }}" class="text-muted text-decoration-none small"><i class="fas fa-lock me-1"></i>Admin Portal</a>', '')
    
    with open('templates/base.html', 'w', encoding='utf-8') as f:
        f.write(base)
        
    print("Base HTML updated")
    
    # 4. Update login.html to add admin hint
    with open('templates/login.html', 'r', encoding='utf-8') as f:
        login_html = f.read()
        
    login_html = login_html.replace('</form>', """</form>
            <div class="mt-3 p-3 bg-light rounded text-center small text-muted">
                <i class="fas fa-info-circle"></i> <strong>Admin Access:</strong><br>Email: admin@smartcart.com<br>Password: admin123
            </div>""")
            
    with open('templates/login.html', 'w', encoding='utf-8') as f:
        f.write(login_html)
        
    print("Login HTML updated")
        
    # 5. Add "Edit" button to shop.html cards for admins
    with open('templates/shop.html', 'r', encoding='utf-8') as f:
        shop_html = f.read()
        
    old_btn = '<a href="{{ url_for(\'product\', product_id=prod.id) }}" class="btn btn-dark rounded-circle" style="width: 40px; height: 40px; padding: 8px;"><i class="fas fa-plus"></i></a>'
    new_btn = """{% if session.is_admin %}
        <a href="{{ url_for('admin_edit_product', product_id=prod.id) }}" class="btn btn-warning rounded-circle shadow-sm" style="width: 40px; height: 40px; padding: 8px;" title="Edit Product"><i class="fas fa-edit"></i></a>
    {% else %}
        <a href="{{ url_for('product', product_id=prod.id) }}" class="btn btn-dark rounded-circle shadow-sm" style="width: 40px; height: 40px; padding: 8px;"><i class="fas fa-plus"></i></a>
    {% endif %}"""
    
    shop_html = shop_html.replace(old_btn, new_btn)
    with open('templates/shop.html', 'w', encoding='utf-8') as f:
        f.write(shop_html)

if __name__ == '__main__':
    merge_logins()
