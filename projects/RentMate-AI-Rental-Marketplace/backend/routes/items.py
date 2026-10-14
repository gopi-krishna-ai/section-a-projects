from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Item, Category, User, SearchHistory
from ai.matcher import matcher
from ai.price_assistant import price_assistant

items_bp = Blueprint('items', __name__)

@items_bp.route('/', methods=['GET'])
def get_items():
    category = request.args.get('category')
    query = Item.query.filter_by(status='APPROVED')
    if category:
        query = query.filter_by(category=category)
    items = query.all()
    
    result = []
    for item in items:
        owner = User.query.get(item.owner_id)
        result.append({
            'id': item.id,
            'name': item.name,
            'category': item.category,
            'description': item.description,
            'price_per_day': item.price_per_day,
            'location': item.location,
            'owner_name': owner.name,
            'owner_rating': 4.5 # Mock rating
        })
    return jsonify(result), 200

@items_bp.route('/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = Item.query.get_or_404(item_id)
    owner = User.query.get(item.owner_id)
    return jsonify({
        'id': item.id,
        'name': item.name,
        'category': item.category,
        'description': item.description,
        'price_per_day': item.price_per_day,
        'security_deposit': item.security_deposit,
        'location': item.location,
        'condition': item.condition,
        'image_url': item.image_url,
        'owner_name': owner.name,
        'owner_id': owner.id,
        'status': item.status
    }), 200

@items_bp.route('/', methods=['POST'])
@jwt_required()
def create_item():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if user.role != 'OWNER':
        return jsonify({'error': 'Only owners can create items'}), 403
        
    data = request.get_json()
    new_item = Item(
        owner_id=user.id,
        name=data.get('name'),
        category=data.get('category'),
        description=data.get('description'),
        condition=data.get('condition'),
        price_per_day=data.get('price_per_day'),
        location=data.get('location'),
        image_url=data.get('image_url'),
        status='PENDING_APPROVAL'
    )
    db.session.add(new_item)
    db.session.commit()
    return jsonify({'message': 'Item created, pending approval', 'id': new_item.id}), 201

@items_bp.route('/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    return jsonify([c.name for c in categories]), 200

@items_bp.route('/ai/match', methods=['POST'])
@jwt_required()
def ai_match():
    user_id = get_jwt_identity()
    data = request.get_json()
    query = data.get('query', '')
    
    # Log search history
    history = SearchHistory(user_id=user_id, query=query)
    db.session.add(history)
    db.session.commit()
    
    active_items = Item.query.filter_by(status='APPROVED').all()
    matches = matcher.find_matches(query, active_items)
    
    result = []
    for m in matches:
        item = m['item']
        owner = User.query.get(item.owner_id)
        result.append({
            'item': {
                'id': item.id,
                'name': item.name,
                'category': item.category,
                'description': item.description,
                'price_per_day': item.price_per_day,
                'location': item.location,
                'image_url': item.image_url,
                'owner_name': owner.name
            },
            'match_score': m['match_score'],
            'reasons': m['reasons']
        })
        
    return jsonify({'query': query, 'matches': result}), 200

@items_bp.route('/ai/price-suggest', methods=['POST'])
@jwt_required()
def price_suggest():
    data = request.get_json()
    category = data.get('category')
    name = data.get('name')
    condition = data.get('condition', 'Good')
    
    suggestion = price_assistant.suggest_price(category, name, condition)
    return jsonify(suggestion), 200

@items_bp.route('/owner', methods=['GET'])
@jwt_required()
def get_owner_items():
    user_id = get_jwt_identity()
    items = Item.query.filter_by(owner_id=user_id).all()
    return jsonify([{
        'id': i.id, 'name': i.name, 'status': i.status, 'price_per_day': i.price_per_day, 'category': i.category
    } for i in items]), 200
