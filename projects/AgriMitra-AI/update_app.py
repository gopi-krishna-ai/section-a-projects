import re

with open('app.py', 'r', encoding='utf-8') as f:
    app_py = f.read()

# 1. Add Product model
product_model = """
class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    item_type = db.Column(db.String(50), nullable=False) # 'seed' or 'fertilizer'
    item_name = db.Column(db.String(100), nullable=False) # e.g. 'Coffee', 'Rice', '10-26-26'
    seller = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(500), nullable=False)
"""
if "class Product" not in app_py:
    app_py = app_py.replace('class PredictionHistory(db.Model):', product_model + '\n\nclass PredictionHistory(db.Model):')

# 2. Add Routes
admin_routes = """
import werkzeug
import os
from werkzeug.utils import secure_filename

app.config['UPLOAD_FOLDER'] = os.path.join(BASE_DIR, 'static', 'uploads')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route("/admin")
def admin_dashboard():
    return render_template("admin.html")

@app.route("/api/admin/product", methods=["POST"])
def add_product():
    try:
        item_type = request.form.get("item_type")
        item_name = request.form.get("item_name")
        seller = request.form.get("seller")
        description = request.form.get("description")
        price = float(request.form.get("price"))
        
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
            image_url=image_url
        )
        db.session.add(product)
        db.session.commit()
        return jsonify({"success": True, "message": "Product added successfully!"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400

@app.route("/api/products", methods=["GET"])
def get_products():
    products = Product.query.all()
    return jsonify([{
        "id": p.id,
        "item_type": p.item_type,
        "item_name": p.item_name,
        "seller": p.seller,
        "description": p.description,
        "price": p.price,
        "image_url": p.image_url
    } for p in products])
"""

if "def admin_dashboard():" not in app_py:
    # Insert before # ---------------------------------------------------------------------------
    # Helpers
    app_py = app_py.replace("# Helpers", admin_routes + "\n# Helpers")

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(app_py)

print("App.py updated with Admin and Products functionality.")
