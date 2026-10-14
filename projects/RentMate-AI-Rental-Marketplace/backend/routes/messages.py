from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Message, User, RentalRequest

messages_bp = Blueprint('messages', __name__)

@messages_bp.route('/contacts', methods=['GET'])
@jwt_required()
def get_contacts():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    contacts = []
    seen = set()

    if user.role == 'RENTER':
        # Get delivery guys for active rentals
        rentals = RentalRequest.query.filter_by(renter_id=user.id).all()
        for r in rentals:
            if r.delivery_guy_id and r.delivery_guy_id not in seen:
                seen.add(r.delivery_guy_id)
                dg = User.query.get(r.delivery_guy_id)
                contacts.append({'id': dg.id, 'name': dg.name, 'role': dg.role, 'rental_context': r.item.name})
    elif user.role == 'OWNER':
        # Get delivery guys for items they are renting out
        rentals = RentalRequest.query.filter_by(owner_id=user.id).all()
        for r in rentals:
            if r.delivery_guy_id and r.delivery_guy_id not in seen:
                seen.add(r.delivery_guy_id)
                dg = User.query.get(r.delivery_guy_id)
                contacts.append({'id': dg.id, 'name': dg.name, 'role': dg.role, 'rental_context': f"{r.item.name} (Pick-up)"})
    elif user.role == 'DELIVERY':
        # Get both renters and owners for active tasks
        rentals = RentalRequest.query.filter_by(delivery_guy_id=user.id).all()
        for r in rentals:
            if r.renter_id and r.renter_id not in seen:
                seen.add(r.renter_id)
                r_user = User.query.get(r.renter_id)
                contacts.append({'id': r_user.id, 'name': r_user.name, 'role': r_user.role, 'rental_context': f"{r.item.name} (Drop-off)"})
            if r.owner_id and r.owner_id not in seen:
                seen.add(r.owner_id)
                o_user = User.query.get(r.owner_id)
                contacts.append({'id': o_user.id, 'name': o_user.name, 'role': o_user.role, 'rental_context': f"{r.item.name} (Pick-up)"})
    
    # We remove customer to customer inbox, so we don't return owners for renters, etc.

    return jsonify(contacts), 200


@messages_bp.route('/<int:other_user_id>', methods=['GET'])
@jwt_required()
def get_messages(other_user_id):
    user_id = get_jwt_identity()
    
    msgs = Message.query.filter(
        ((Message.sender_id == user_id) & (Message.receiver_id == other_user_id)) |
        ((Message.sender_id == other_user_id) & (Message.receiver_id == user_id))
    ).order_by(Message.created_at.asc()).all()
    
    return jsonify([{
        'id': m.id,
        'sender_id': m.sender_id,
        'receiver_id': m.receiver_id,
        'content': m.content,
        'created_at': m.created_at.isoformat()
    } for m in msgs]), 200


@messages_bp.route('/<int:other_user_id>', methods=['POST'])
@jwt_required()
def send_message(other_user_id):
    user_id = get_jwt_identity()
    data = request.get_json()
    content = data.get('content')
    
    if not content:
        return jsonify({'error': 'Content is required'}), 400
        
    msg = Message(sender_id=user_id, receiver_id=other_user_id, content=content)
    db.session.add(msg)
    db.session.commit()
    
    return jsonify({
        'id': msg.id,
        'sender_id': msg.sender_id,
        'receiver_id': msg.receiver_id,
        'content': msg.content,
        'created_at': msg.created_at.isoformat()
    }), 201
