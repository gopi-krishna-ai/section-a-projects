from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from models import db
from config import Config
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    CORS(app)
    db.init_app(app)
    jwt = JWTManager(app)

    from routes.auth import auth_bp
    from routes.items import items_bp
    from routes.rentals import rentals_bp
    from routes.admin import admin_bp
    from routes.delivery import delivery_bp
    from routes.messages import messages_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(items_bp, url_prefix='/api/items')
    app.register_blueprint(rentals_bp, url_prefix='/api/rentals')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(delivery_bp, url_prefix='/api/delivery')
    app.register_blueprint(messages_bp, url_prefix='/api/messages')

    @app.route('/api/health', methods=['GET'])
    def health_check():
        return jsonify({"status": "healthy"}), 200

    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True, use_reloader=False, port=5002)
