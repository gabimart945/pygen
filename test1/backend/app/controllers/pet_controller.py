from flask import Blueprint, request, jsonify
from app.services.pet_service import PetService

pet_bp = Blueprint('pet_bp', __name__)

# Initialize service
service = PetService()

# GET all
@pet_bp.route('/', methods=['GET'])
def get_all_pets():
    items = service.get_all()
    return jsonify(items), 200

# GET by ID
@pet_bp.route('/<int:id>', methods=['GET'])
def get_pet(id):
    item = service.get_by_id(id)
    if not item:
        return jsonify({'error': 'Pet not found'}), 404
    return jsonify(item), 200

# POST (Create)
@pet_bp.route('/', methods=['POST'])
def create_pet():
    data = request.get_json()
    item = service.create(data)
    if not item:
        return jsonify({'error': 'Error creating pet'}), 400
    return jsonify(item), 201

# PUT (Update)
@pet_bp.route('/<int:id>', methods=['PUT'])
def update_pet(id):
    data = request.get_json()
    item = service.update(id, data)
    if not item:
        return jsonify({'error': 'Pet not found'}), 404
    return jsonify(item), 200

# DELETE
@pet_bp.route('/<int:id>', methods=['DELETE'])
def delete_pet(id):
    success = service.delete(id)
    if not success:
        return jsonify({'error': 'Pet not found'}), 404
    return '', 204


# GET related owners for pet
@pet_bp.route('/<int:id>/owners', methods=['GET'])
def get_owners_for_pet(id):
    related_items = service.get_owners_for_pet(id)
    if related_items is None:
        return jsonify({'error': 'Related items not found'}), 404
    return jsonify(related_items), 200

# POST related owner for pet
@pet_bp.route('/<int:id>/owners', methods=['POST'])
def add_owner_to_pet(id):
    data = request.get_json()
    related_item = service.add_owner_to_pet(id, data)
    if not related_item:
        return jsonify({'error': 'Error adding related item'}), 400
    return jsonify(related_item), 201

# GET related pettypes for pet
@pet_bp.route('/<int:id>/pettypes', methods=['GET'])
def get_pettypes_for_pet(id):
    related_items = service.get_pettypes_for_pet(id)
    if related_items is None:
        return jsonify({'error': 'Related items not found'}), 404
    return jsonify(related_items), 200

# POST related pettype for pet
@pet_bp.route('/<int:id>/pettypes', methods=['POST'])
def add_pettype_to_pet(id):
    data = request.get_json()
    related_item = service.add_pettype_to_pet(id, data)
    if not related_item:
        return jsonify({'error': 'Error adding related item'}), 400
    return jsonify(related_item), 201

# GET related visitss for pet
@pet_bp.route('/<int:id>/visitss', methods=['GET'])
def get_visitss_for_pet(id):
    related_items = service.get_visitss_for_pet(id)
    if related_items is None:
        return jsonify({'error': 'Related items not found'}), 404
    return jsonify(related_items), 200

# POST related visits for pet
@pet_bp.route('/<int:id>/visitss', methods=['POST'])
def add_visits_to_pet(id):
    data = request.get_json()
    related_item = service.add_visits_to_pet(id, data)
    if not related_item:
        return jsonify({'error': 'Error adding related item'}), 400
    return jsonify(related_item), 201
