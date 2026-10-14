from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False) # RENTER, OWNER, ADMIN, DELIVERY
    phone = db.Column(db.String(20))
    location = db.Column(db.String(100))
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)
    status = db.Column(db.String(20), default='ACTIVE')
    eco_score = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    items = db.relationship('Item', backref='owner', lazy=True)
    rental_requests_as_renter = db.relationship('RentalRequest', foreign_keys='RentalRequest.renter_id', backref='renter', lazy=True)
    rental_requests_as_owner = db.relationship('RentalRequest', foreign_keys='RentalRequest.owner_id', backref='owner_rel', lazy=True)
    delivery_jobs = db.relationship('RentalRequest', foreign_keys='RentalRequest.delivery_guy_id', backref='delivery_guy', lazy=True)

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category = db.Column(db.String(50), nullable=False) # Keep simple string category
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    condition = db.Column(db.String(50))
    price_per_day = db.Column(db.Float, nullable=False)
    security_deposit = db.Column(db.Float, default=0.0)
    quantity = db.Column(db.Integer, default=1)
    location = db.Column(db.String(100))
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)
    image_url = db.Column(db.String(255))
    status = db.Column(db.String(20), default='PENDING_APPROVAL') # PENDING_APPROVAL, APPROVED, REJECTED
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    rental_requests = db.relationship('RentalRequest', backref='item', lazy=True)

class RentalRequest(db.Model):
    __tablename__ = 'rental_requests'
    id = db.Column(db.Integer, primary_key=True)
    renter_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)
    delivery_guy_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    rental_days = db.Column(db.Integer, nullable=False)
    price_per_day = db.Column(db.Float, nullable=False)
    security_deposit = db.Column(db.Float, default=0.0)
    platform_fee = db.Column(db.Float, default=0.0)
    total_amount = db.Column(db.Float, nullable=False)
    
    status = db.Column(db.String(20), default='PENDING') # PENDING, APPROVED, REJECTED, ACTIVE, COMPLETED, CANCELLED
    delivery_status = db.Column(db.String(20), default='PENDING_PICKUP') # PENDING_PICKUP, IN_TRANSIT, DELIVERED
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    rental_id = db.Column(db.Integer, db.ForeignKey('rental_requests.id'), nullable=False)
    reviewer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    reviewee_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False) # 1-5
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class SearchHistory(db.Model):
    __tablename__ = 'search_history'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id')) # Optional
    query = db.Column(db.Text, nullable=False)
    extracted_requirements = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    rental_id = db.Column(db.Integer, db.ForeignKey('rental_requests.id'), nullable=True) # Optional context
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    sender = db.relationship('User', foreign_keys=[sender_id], backref='sent_messages')
    receiver = db.relationship('User', foreign_keys=[receiver_id], backref='received_messages')
