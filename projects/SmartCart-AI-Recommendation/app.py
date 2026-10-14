import os
os.environ["DISABLE_SQLALCHEMY_CEXT"] = "1"
from flask import Flask, render_template, request, session, redirect, url_for, jsonify, flash
from werkzeug.security import generate_password_hash, check_password_hash
from backend.models import db, Customer, Category, Product, Interaction, Order, OrderItem, CartItem, WishlistItem

# Initialize Flask app
app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'smartcart_super_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///smartcart.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

from backend.routes import init_routes
init_routes(app)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
