from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    password_hash = db.Column(db.String(256))
    green_points = db.Column(db.Integer, default=0)
    persona = db.Column(db.String(255)) # E.g., 'Eco-friendly', 'Electronics lover'
    is_admin = db.Column(db.Boolean, default=False)
    
    orders = db.relationship('Order', backref='user', lazy=True)
    interactions = db.relationship('Interaction', backref='user', lazy=True)
    recycling_requests = db.relationship('RecyclingRequest', backref='user', lazy=True)

class Product(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(100))
    material_type = db.Column(db.String(100))
    recycled_content_pct = db.Column(db.Float)
    recyclability_pct = db.Column(db.Float)
    manufacturing_process = db.Column(db.String(100))
    energy_efficiency_score = db.Column(db.Float)
    packaging_type = db.Column(db.String(100))
    packaging_recyclable_pct = db.Column(db.Float)
    carbon_footprint_kg = db.Column(db.Float)
    water_usage_liters = db.Column(db.Float)
    durability_years = db.Column(db.Float)
    price_inr = db.Column(db.Float)
    eco_score = db.Column(db.Float)
    eco_label = db.Column(db.String(50))
    
    image_url = db.Column(db.String(255))
    description = db.Column(db.Text)

class Interaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.String(50), db.ForeignKey('product.id'), nullable=False)
    event_type = db.Column(db.String(50)) # VIEW, CART, PURCHASE
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    avg_eco_score = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    items = db.relationship('OrderItem', backref='order', lazy=True)

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.String(50), db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    price_at_purchase = db.Column(db.Float, nullable=False)

class RecyclingRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.String(50), db.ForeignKey('product.id'), nullable=False)
    purchase_date = db.Column(db.DateTime)
    condition = db.Column(db.String(100))
    reason = db.Column(db.Text)
    status = db.Column(db.String(50), default='Pending Verification') # Pending, Verified
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
