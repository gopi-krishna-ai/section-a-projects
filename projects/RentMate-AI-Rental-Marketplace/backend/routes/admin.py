from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User, Item, RentalRequest, SearchHistory
from sqlalchemy import func

admin_bp = Blueprint('admin', __name__)

def check_admin():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user or user.role != 'ADMIN':
        return False
    return True

@admin_bp.route('/analytics', methods=['GET'])
@jwt_required()
def get_analytics():
    if not check_admin():
        return jsonify({'error': 'Unauthorized'}), 403
        
    total_users = User.query.count()
    total_items = Item.query.count()
    total_rentals = RentalRequest.query.count()
    
    # Revenue (platform fees sum for completed/approved)
    completed = RentalRequest.query.filter(RentalRequest.status.in_(['APPROVED', 'COMPLETED'])).all()
    revenue = sum([r.total_amount for r in completed])
    
    # Rentals by category
    cats = db.session.query(Item.category, func.count(Item.id)).group_by(Item.category).all()
    categories_data = [{"name": c[0], "value": c[1]} for c in cats]
    
    return jsonify({
        'total_users': total_users,
        'total_items': total_items,
        'total_rentals': total_rentals,
        'total_revenue': revenue,
        'categories_data': categories_data
    }), 200

@admin_bp.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    if not check_admin(): return jsonify({'error': 'Unauthorized'}), 403
    users = User.query.all()
    return jsonify([{
        'id': u.id, 'name': u.name, 'email': u.email, 'role': u.role, 'status': u.status, 'eco_score': u.eco_score
    } for u in users]), 200

@admin_bp.route('/items', methods=['GET'])
@jwt_required()
def get_all_items():
    if not check_admin(): return jsonify({'error': 'Unauthorized'}), 403
    items = Item.query.all()
    return jsonify([{
        'id': i.id, 'name': i.name, 'category': i.category, 'status': i.status, 'price_per_day': i.price_per_day
    } for i in items]), 200

@admin_bp.route('/items/<int:item_id>/status', methods=['PUT'])
@jwt_required()
def update_item_status(item_id):
    if not check_admin(): return jsonify({'error': 'Unauthorized'}), 403
    item = Item.query.get_or_404(item_id)
    status = request.get_json().get('status')
    if status in ['APPROVED', 'REJECTED']:
        item.status = status
        db.session.commit()
    return jsonify({'message': 'Status updated'})

@admin_bp.route('/rentals', methods=['GET'])
@jwt_required()
def get_all_rentals():
    if not check_admin(): return jsonify({'error': 'Unauthorized'}), 403
    rentals = RentalRequest.query.all()
    result = []
    for r in rentals:
        item = Item.query.get(r.item_id)
        result.append({
            'id': r.id,
            'item_name': item.name,
            'start_date': r.start_date.isoformat(),
            'end_date': r.end_date.isoformat(),
            'total_amount': r.total_amount,
            'status': r.status
        })
    return jsonify(result), 200
