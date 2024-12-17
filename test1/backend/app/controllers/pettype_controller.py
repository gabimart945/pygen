from flask import Blueprint, request, jsonify
from app.services.pettype_service import PetTypeService

pettype_bp = Blueprint('pettype_bp', __name__)

# Initialize service
service = PetTypeService()

# GET all
@pettype_bp.route('/', methods=['GET'])
def get_all_pettypes():
    items = service.get_all()
    return jsonify(items), 200

# GET by ID
@pettype_bp.route('/<int:id>', methods=['GET'])
def get_pettype(id):
    item = service.get_by_id(id)
    if not item:
        return jsonify({'error': 'PetType not found'}), 404
    return jsonify(item), 200

# POST (Create)
@pettype_bp.route('/', methods=['POST'])
def create_pettype():
    data = request.get_json()
    item = service.create(data)
    if not item:
        return jsonify({'error': 'Error creating pettype'}), 400
    return jsonify(item), 201

# PUT (Update)
@pettype_bp.route('/<int:id>', methods=['PUT'])
def update_pettype(id):
    data = request.get_json()
    item = service.update(id, data)
    if not item:
        return jsonify({'error': 'PetType not found'}), 404
    return jsonify(item), 200

# DELETE
@pettype_bp.route('/<int:id>', methods=['DELETE'])
def delete_pettype(id):
    success = service.delete(id)
    if not success:
        return jsonify({'error': 'PetType not found'}), 404
    return '', 204


# GET related petss for pettype
@pettype_bp.route('/<int:id>/petss', methods=['GET'])
def get_petss_for_pettype(id):
    related_items = service.get_petss_for_pettype(id)
    if related_items is None:
        return jsonify({'error': 'Related items not found'}), 404
    return jsonify(related_items), 200

# POST related pets for pettype
@pettype_bp.route('/<int:id>/petss', methods=['POST'])
def add_pets_to_pettype(id):
    data = request.get_json()
    related_item = service.add_pets_to_pettype(id, data)
    if not related_item:
        return jsonify({'error': 'Error adding related item'}), 400
    return jsonify(related_item), 201
