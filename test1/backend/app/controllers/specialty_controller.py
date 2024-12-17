from flask import Blueprint, request, jsonify
from app.services.specialty_service import SpecialtyService

specialty_bp = Blueprint('specialty_bp', __name__)

# Initialize service
service = SpecialtyService()

# GET all
@specialty_bp.route('/', methods=['GET'])
def get_all_specialtys():
    items = service.get_all()
    return jsonify(items), 200

# GET by ID
@specialty_bp.route('/<int:id>', methods=['GET'])
def get_specialty(id):
    item = service.get_by_id(id)
    if not item:
        return jsonify({'error': 'Specialty not found'}), 404
    return jsonify(item), 200

# POST (Create)
@specialty_bp.route('/', methods=['POST'])
def create_specialty():
    data = request.get_json()
    item = service.create(data)
    if not item:
        return jsonify({'error': 'Error creating specialty'}), 400
    return jsonify(item), 201

# PUT (Update)
@specialty_bp.route('/<int:id>', methods=['PUT'])
def update_specialty(id):
    data = request.get_json()
    item = service.update(id, data)
    if not item:
        return jsonify({'error': 'Specialty not found'}), 404
    return jsonify(item), 200

# DELETE
@specialty_bp.route('/<int:id>', methods=['DELETE'])
def delete_specialty(id):
    success = service.delete(id)
    if not success:
        return jsonify({'error': 'Specialty not found'}), 404
    return '', 204


# GET related vets for specialty
@specialty_bp.route('/<int:id>/vets', methods=['GET'])
def get_vets_for_specialty(id):
    related_items = service.get_vets_for_specialty(id)
    if related_items is None:
        return jsonify({'error': 'Related items not found'}), 404
    return jsonify(related_items), 200

# POST related vet for specialty
@specialty_bp.route('/<int:id>/vets', methods=['POST'])
def add_vet_to_specialty(id):
    data = request.get_json()
    related_item = service.add_vet_to_specialty(id, data)
    if not related_item:
        return jsonify({'error': 'Error adding related item'}), 400
    return jsonify(related_item), 201
