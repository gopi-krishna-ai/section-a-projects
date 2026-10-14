import os

def append_admin_routes():
    with open('backend/routes.py', 'r', encoding='utf-8') as f:
        content = f.read()

    # If already injected, skip
    if '@app.route(\'/admin/dashboard\')' in content:
        print("Admin routes already exist.")
        return

    # Add imports if not present
    if 'from werkzeug.utils import secure_filename' not in content:
        content = content.replace(
            'from flask import render_template, request, session, redirect, url_for, flash',
            'from flask import render_template, request, session, redirect, url_for, flash\nfrom werkzeug.utils import secure_filename\nimport os'
        )

    admin_routes = """
    # --- ADMIN PANEL ROUTES ---
    
    @app.route('/admin/login', methods=['GET', 'POST'])
    def admin_login():
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            # Hardcoded demo admin
            if username == 'admin' and password == 'admin123':
                session['is_admin'] = True
                flash("Admin login successful!", "success")
                return redirect(url_for('admin_dashboard'))
            else:
                flash("Invalid admin credentials.", "danger")
        return render_template('admin_login.html')
        
    @app.route('/admin/logout')
    def admin_logout():
        session.pop('is_admin', None)
        flash("Admin logged out.", "info")
        return redirect(url_for('index'))

    @app.route('/admin/dashboard')
    def admin_dashboard():
        if not session.get('is_admin'):
            flash("Admin access required.", "danger")
            return redirect(url_for('admin_login'))
            
        products = Product.query.all()
        return render_template('admin_dashboard.html', products=products)
        
    @app.route('/admin/add_product', methods=['GET', 'POST'])
    def admin_add_product():
        if not session.get('is_admin'):
            return redirect(url_for('admin_login'))
            
        categories = Category.query.all()
        
        if request.method == 'POST':
            name = request.form.get('name')
            category_id = request.form.get('category_id')
            price = float(request.form.get('price'))
            description = request.form.get('description')
            
            # Handle image upload
            image_file = request.files.get('image')
            image_url = "https://placehold.co/500x500/png?text=No+Image"
            
            if image_file and image_file.filename != '':
                filename = secure_filename(image_file.filename)
                upload_folder = os.path.join(app.root_path, 'static', 'uploads')
                os.makedirs(upload_folder, exist_ok=True)
                image_file.save(os.path.join(upload_folder, filename))
                image_url = 'uploads/' + filename
                
            new_prod = Product(
                name=name,
                category_id=category_id,
                price=price,
                description=description,
                image_url=image_url,
                rating=5.0,
                review_count=0
            )
            db.session.add(new_prod)
            db.session.commit()
            flash("Product added successfully!", "success")
            return redirect(url_for('admin_dashboard'))
            
        return render_template('admin_add_product.html', categories=categories)
        
    @app.route('/admin/edit_product/<int:product_id>', methods=['GET', 'POST'])
    def admin_edit_product(product_id):
        if not session.get('is_admin'):
            return redirect(url_for('admin_login'))
            
        prod = Product.query.get_or_404(product_id)
        categories = Category.query.all()
        
        if request.method == 'POST':
            prod.name = request.form.get('name')
            prod.category_id = request.form.get('category_id')
            prod.price = float(request.form.get('price'))
            prod.description = request.form.get('description')
            
            image_file = request.files.get('image')
            if image_file and image_file.filename != '':
                filename = secure_filename(image_file.filename)
                upload_folder = os.path.join(app.root_path, 'static', 'uploads')
                os.makedirs(upload_folder, exist_ok=True)
                image_file.save(os.path.join(upload_folder, filename))
                prod.image_url = 'uploads/' + filename
                
            db.session.commit()
            flash("Product updated successfully!", "success")
            return redirect(url_for('admin_dashboard'))
            
        return render_template('admin_edit_product.html', product=prod, categories=categories)
"""

    # We need to insert this right before the last line or before `except Exception as e:` inside `init_routes(app)`?
    # Wait, `init_routes(app)` just defines functions inside. I can append it before the end of the file.
    # Since `init_routes` encapsulates all routes, I must ensure indentation matches (4 spaces).
    
    # Let's just find `return render_template('recommendations.html', recommendations=recs` which is at the end.
    
    content = content + "\n" + admin_routes
    
    with open('backend/routes.py', 'w', encoding='utf-8') as f:
        f.write(content)
        
    print("Admin routes added!")

if __name__ == '__main__':
    append_admin_routes()
