from flask import Blueprint, request, jsonify
from models import db, RentalRequest, User, Item
from flask_jwt_extended import jwt_required, get_jwt_identity

delivery_bp = Blueprint('delivery', __name__)

@delivery_bp.route('/tasks', methods=['GET'])
@jwt_required()
def get_delivery_tasks():
    user_id = get_jwt_identity()
    current_user = User.query.get(user_id)
    if current_user.role != 'DELIVERY':
        return jsonify({'message': 'Unauthorized'}), 403

    # Get all active rentals that need delivery or are already assigned to this delivery guy
    tasks = RentalRequest.query.filter(
        RentalRequest.status == 'ACTIVE',
        db.or_(
            RentalRequest.delivery_guy_id == None,
            RentalRequest.delivery_guy_id == current_user.id
        )
    ).all()

    task_list = []
    for task in tasks:
        owner = User.query.get(task.owner_id)
        renter = User.query.get(task.renter_id)
        item = Item.query.get(task.item_id)
        
        task_list.append({
            'id': task.id,
            'item_name': item.name,
            'item_image': item.image_url,
            'owner': {
                'name': owner.name,
                'phone': owner.phone,
                'location': owner.location,
                'lat': owner.lat,
                'lng': owner.lng
            },
            'renter': {
                'name': renter.name,
                'phone': renter.phone,
                'location': renter.location,
                'lat': renter.lat,
                'lng': renter.lng
            },
            'delivery_guy_id': task.delivery_guy_id,
            'delivery_status': task.delivery_status
        })

    return jsonify(task_list), 200

@delivery_bp.route('/accept/<int:task_id>', methods=['POST'])
@jwt_required()
def accept_task(task_id):
    user_id = get_jwt_identity()
    current_user = User.query.get(user_id)
    if current_user.role != 'DELIVERY':
        return jsonify({'message': 'Unauthorized'}), 403

    task = RentalRequest.query.get_or_404(task_id)
    if task.delivery_guy_id is not None and task.delivery_guy_id != current_user.id:
        return jsonify({'message': 'Task already accepted by someone else'}), 400

    task.delivery_guy_id = current_user.id
    task.delivery_status = 'PENDING_PICKUP'
    db.session.commit()
    
    return jsonify({'message': 'Task accepted successfully'}), 200

@delivery_bp.route('/update/<int:task_id>', methods=['POST'])
@jwt_required()
def update_task_status(task_id):
    user_id = get_jwt_identity()
    current_user = User.query.get(user_id)
    if current_user.role != 'DELIVERY':
        return jsonify({'message': 'Unauthorized'}), 403

    task = RentalRequest.query.get_or_404(task_id)
    if task.delivery_guy_id != current_user.id:
        return jsonify({'message': 'Unauthorized to update this task'}), 403

    data = request.get_json()
    new_status = data.get('status')
    
    if new_status not in ['PENDING_PICKUP', 'IN_TRANSIT', 'DELIVERED']:
        return jsonify({'message': 'Invalid status'}), 400

    task.delivery_status = new_status
    db.session.commit()
    
    return jsonify({'message': 'Task status updated successfully'}), 200
