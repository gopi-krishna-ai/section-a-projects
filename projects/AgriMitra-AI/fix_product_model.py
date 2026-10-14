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
    image_url = db.Column(db.String(500), nullable=False)
    stock = db.Column(db.Integer, default=100)
    discount = db.Column(db.Integer, default=0)"""

content = re.sub(r'class Product\(db\.Model\):[\s\S]*?image_url = db\.Column\(db\.String\(500\), nullable=False\)', product_replacement, content)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('Updated Product model successfully!')
