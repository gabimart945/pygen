from flask import Blueprint, request, jsonify
from app.services.owner_service import OwnerService

owner_bp = Blueprint('owner_bp', __name__)

# Initialize service
service = OwnerService()

# GET all
@owner_bp.route('/', methods=['GET'])
def get_all_owners():
    items = service.get_all()
    return jsonify(items), 200

# GET by ID
@owner_bp.route('/<int:id>', methods=['GET'])
def get_owner(id):
    item = service.get_by_id(id)
    if not item:
        return jsonify({'error': 'Owner not found'}), 404
    return jsonify(item), 200

# POST (Create)
@owner_bp.route('/', methods=['POST'])
def create_owner():
    data = request.get_json()
    item = service.create(data)
    if not item:
        return jsonify({'error': 'Error creating owner'}), 400
    return jsonify(item), 201

# PUT (Update)
@owner_bp.route('/<int:id>', methods=['PUT'])
def update_owner(id):
    data = request.get_json()
    item = service.update(id, data)
    if not item:
        return jsonify({'error': 'Owner not found'}), 404
    return jsonify(item), 200

# DELETE
@owner_bp.route('/<int:id>', methods=['DELETE'])
def delete_owner(id):
    success = service.delete(id)
    if not success:
        return jsonify({'error': 'Owner not found'}), 404
    return '', 204


# GET related petss for owner
@owner_bp.route('/<int:id>/petss', methods=['GET'])
def get_petss_for_owner(id):
    related_items = service.get_petss_for_owner(id)
    if related_items is None:
        return jsonify({'error': 'Related items not found'}), 404
    return jsonify(related_items), 200

# POST related pets for owner
@owner_bp.route('/<int:id>/petss', methods=['POST'])
def add_pets_to_owner(id):
    data = request.get_json()
    related_item = service.add_pets_to_owner(id, data)
    if not related_item:
        return jsonify({'error': 'Error adding related item'}), 400
    return jsonify(related_item), 201
