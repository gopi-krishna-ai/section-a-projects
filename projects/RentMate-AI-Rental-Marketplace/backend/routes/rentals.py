from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, RentalRequest, Item, User
from datetime import datetime

rentals_bp = Blueprint('rentals', __name__)

@rentals_bp.route('/', methods=['POST'])
@jwt_required()
def request_rental():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if user.role != 'RENTER':
        return jsonify({'error': 'Only renters can request items'}), 403
        
    data = request.get_json()
    item_id = data.get('item_id')
    start_str = data.get('start_date')
    end_str = data.get('end_date')
    
    item = Item.query.get_or_404(item_id)
    if item.status != 'APPROVED':
        return jsonify({'error': 'Item is not available'}), 400
        
    start_date = datetime.fromisoformat(start_str.replace('Z', '+00:00'))
    end_date = datetime.fromisoformat(end_str.replace('Z', '+00:00'))
    
    # Calculate days (inclusive)
    days = (end_date.date() - start_date.date()).days + 1
    if days < 1:
        return jsonify({'error': 'Invalid dates'}), 400
        
    # Check overlaps (simple logic for demo)
    overlaps = RentalRequest.query.filter(
        RentalRequest.item_id == item_id,
        RentalRequest.status.in_(['APPROVED', 'ACTIVE']),
        RentalRequest.start_date <= end_date,
        RentalRequest.end_date >= start_date
    ).all()
    
    if overlaps:
        return jsonify({'error': 'Item is already booked for these dates'}), 400
        
    price = item.price_per_day
    subtotal = price * days
    platform_fee = 10.0 # Fixed for demo
    total = subtotal + item.security_deposit + platform_fee
    
    rental = RentalRequest(
        renter_id=user.id,
        owner_id=item.owner_id,
        item_id=item.id,
        start_date=start_date,
        end_date=end_date,
        rental_days=days,
        price_per_day=price,
        security_deposit=item.security_deposit,
        platform_fee=platform_fee,
        total_amount=total,
        status='PENDING'
    )
    
    db.session.add(rental)
    db.session.commit()
    
    return jsonify({'message': 'Rental requested successfully', 'id': rental.id}), 201

@rentals_bp.route('/my-requests', methods=['GET'])
@jwt_required()
def get_my_rentals():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if user.role == 'RENTER':
        rentals = RentalRequest.query.filter_by(renter_id=user.id).order_by(RentalRequest.created_at.desc()).all()
    else:
        rentals = RentalRequest.query.filter_by(owner_id=user.id).order_by(RentalRequest.created_at.desc()).all()
        
    result = []
    for r in rentals:
        item = Item.query.get(r.item_id)
        other_user = User.query.get(r.owner_id if user.role == 'RENTER' else r.renter_id)
        result.append({
            'id': r.id,
            'item_name': item.name,
            'other_party_name': other_user.name,
            'start_date': r.start_date.isoformat(),
            'end_date': r.end_date.isoformat(),
            'total_amount': r.total_amount,
            'status': r.status
        })
    return jsonify(result), 200

@rentals_bp.route('/<int:request_id>/status', methods=['PUT'])
@jwt_required()
def update_rental_status(request_id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    rental = RentalRequest.query.get_or_404(request_id)
    data = request.get_json()
    new_status = data.get('status')
    
    # Owners can approve/reject, Renters can cancel, Admins can do anything
    if user.role == 'OWNER' and rental.owner_id == user.id:
        if new_status in ['APPROVED', 'REJECTED', 'ACTIVE', 'COMPLETED']:
            rental.status = new_status
            if new_status == 'COMPLETED':
                renter = User.query.get(rental.renter_id)
                renter.eco_score += 5 # Add eco score
            db.session.commit()
            return jsonify({'message': 'Status updated'})
            
    elif user.role == 'ADMIN':
        rental.status = new_status
        db.session.commit()
        return jsonify({'message': 'Status updated'})
        
    return jsonify({'error': 'Unauthorized action'}), 403
