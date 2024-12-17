from flask import Blueprint, request, jsonify
from app.services.visit_service import VisitService

visit_bp = Blueprint('visit_bp', __name__)

# Initialize service
service = VisitService()

# GET all
@visit_bp.route('/', methods=['GET'])
def get_all_visits():
    items = service.get_all()
    return jsonify(items), 200

# GET by ID
@visit_bp.route('/<int:id>', methods=['GET'])
def get_visit(id):
    item = service.get_by_id(id)
    if not item:
        return jsonify({'error': 'Visit not found'}), 404
    return jsonify(item), 200

# POST (Create)
@visit_bp.route('/', methods=['POST'])
def create_visit():
    data = request.get_json()
    item = service.create(data)
    if not item:
        return jsonify({'error': 'Error creating visit'}), 400
    return jsonify(item), 201

# PUT (Update)
@visit_bp.route('/<int:id>', methods=['PUT'])
def update_visit(id):
    data = request.get_json()
    item = service.update(id, data)
    if not item:
        return jsonify({'error': 'Visit not found'}), 404
    return jsonify(item), 200

# DELETE
@visit_bp.route('/<int:id>', methods=['DELETE'])
def delete_visit(id):
    success = service.delete(id)
    if not success:
        return jsonify({'error': 'Visit not found'}), 404
    return '', 204


# GET related pets for visit
@visit_bp.route('/<int:id>/pets', methods=['GET'])
def get_pets_for_visit(id):
    related_items = service.get_pets_for_visit(id)
    if related_items is None:
        return jsonify({'error': 'Related items not found'}), 404
    return jsonify(related_items), 200

# POST related pet for visit
@visit_bp.route('/<int:id>/pets', methods=['POST'])
def add_pet_to_visit(id):
    data = request.get_json()
    related_item = service.add_pet_to_visit(id, data)
    if not related_item:
        return jsonify({'error': 'Error adding related item'}), 400
    return jsonify(related_item), 201
