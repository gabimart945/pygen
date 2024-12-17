from flask import Blueprint, request, jsonify
from app.services.vet_service import VetService

vet_bp = Blueprint('vet_bp', __name__)

# Initialize service
service = VetService()

# GET all
@vet_bp.route('/', methods=['GET'])
def get_all_vets():
    items = service.get_all()
    return jsonify(items), 200

# GET by ID
@vet_bp.route('/<int:id>', methods=['GET'])
def get_vet(id):
    item = service.get_by_id(id)
    if not item:
        return jsonify({'error': 'Vet not found'}), 404
    return jsonify(item), 200

# POST (Create)
@vet_bp.route('/', methods=['POST'])
def create_vet():
    data = request.get_json()
    item = service.create(data)
    if not item:
        return jsonify({'error': 'Error creating vet'}), 400
    return jsonify(item), 201

# PUT (Update)
@vet_bp.route('/<int:id>', methods=['PUT'])
def update_vet(id):
    data = request.get_json()
    item = service.update(id, data)
    if not item:
        return jsonify({'error': 'Vet not found'}), 404
    return jsonify(item), 200

# DELETE
@vet_bp.route('/<int:id>', methods=['DELETE'])
def delete_vet(id):
    success = service.delete(id)
    if not success:
        return jsonify({'error': 'Vet not found'}), 404
    return '', 204


# GET related specialtyss for vet
@vet_bp.route('/<int:id>/specialtyss', methods=['GET'])
def get_specialtyss_for_vet(id):
    related_items = service.get_specialtyss_for_vet(id)
    if related_items is None:
        return jsonify({'error': 'Related items not found'}), 404
    return jsonify(related_items), 200

# POST related specialtys for vet
@vet_bp.route('/<int:id>/specialtyss', methods=['POST'])
def add_specialtys_to_vet(id):
    data = request.get_json()
    related_item = service.add_specialtys_to_vet(id, data)
    if not related_item:
        return jsonify({'error': 'Error adding related item'}), 400
    return jsonify(related_item), 201
