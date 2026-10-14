import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

product_replacement = """class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    item_type = db.Column(db.String(50), nullable=False) # 'seed' or 'fertilizer'
    item_name = db.Column(db.String(100), nullable=False) # e.g. 'Coffee', 'Rice', '10-26-26'
    seller = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(255), nullable=True)
    stock = db.Column(db.Integer, default=100)
    discount = db.Column(db.Integer, default=0)"""

content = re.sub(r'class Product\(db\.Model\):[\s\S]*?image_url = db\.Column\(db\.String\(255\), nullable=True\)', product_replacement, content)

order_models = """
class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default='Pending')
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

class OrderItem(db.Model):
    __tablename__ = "order_items"
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    price = db.Column(db.Float, nullable=False)
"""

if 'class Order(db.Model):' not in content:
    content = content.replace('class PredictionHistory(db.Model):', order_models + '\nclass PredictionHistory(db.Model):')

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('Updated app.py models')
