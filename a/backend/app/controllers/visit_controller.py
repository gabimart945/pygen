from flask import Blueprint, request, jsonify
from app.services.visit_service import VisitService


visit_bp = Blueprint('visit_bp', __name__)
service = VisitService()

# GET all records
@visit_bp.route('/', methods=['GET'])

def get_all_visits():
    items = service.get_all()  # Este método devuelve sólo la lista (sin errores)
    return jsonify(items), 200

# GET a single record by ID
@visit_bp.route('/<int:id>', methods=['GET'])

def get_visit(id):
    item = service.get_by_id(id)  # Este método también devuelve sólo el objeto o None
    if not item:
        return jsonify({'error': 'Visit not found'}), 404
    return jsonify(item), 200

# POST to create a new record
@visit_bp.route('/', methods=['POST'])

def create_visit():
    data = request.get_json()
    item, errors = service.create(data)
    if errors:
        # Si hay errores, normalmente son de validación
        return jsonify({'errors': errors}), 400
    # item es el dict ya serializado desde el servicio
    return jsonify(item), 201

# PUT to update an existing record
@visit_bp.route('/<int:id>', methods=['PUT'])

def update_visit(id):
    data = request.get_json()
    item, errors = service.update(id, data)

    if errors:
        # Si hay errores, pueden ser de validación o algún otro
        return jsonify({'errors': errors}), 400

    if not item:
        # Puede que el servicio retorne (None, None) si no existe la entidad
        return jsonify({'error': 'Visit not found'}), 404

    return jsonify(item), 200

# DELETE to remove a record
@visit_bp.route('/<int:id>', methods=['DELETE'])

def delete_visit(id):
    success = service.delete(id)  # Devuelve True o False
    if not success:
        return jsonify({'error': 'Visit not found'}), 404
    return '', 204


# GET related pet records
@visit_bp.route('/<int:id>/pets', methods=['GET'])
def get_pets(id):
    items, errors = service.get_pets(id)

    # El servicio retorna (None, { 'error': ... }) si no encuentra la entidad padre
    if errors:
        # Podrías chequear si es "not found" u otro tipo de error
        if errors.get('error') == 'Visit not found':
            return jsonify(errors), 404
        # Si fuera un error distinto
        return jsonify({'errors': errors}), 400

    if items is None:
        # Por convención, si items es None pero no hay errors,
        # podrías devolver un 404 o 400 según tu criterio
        return jsonify({'error': 'Failed to fetch related items'}), 400

    return jsonify(items), 200

# POST to add a related pet
@visit_bp.route('/<int:id>/pets', methods=['POST'])

def add_pet(id):
    data = request.get_json()
    item, errors = service.add_pet(id, data)

    if errors:
        # Si errors no es None, puede ser validación o "no se encontró el padre"
        if errors.get('error') == 'Visit not found':
            return jsonify(errors), 404
        # Si son errores de validación u otros
        return jsonify({'errors': errors}), 400

    if not item:
        # Si no existe item y no hay errors, podría ser un error genérico
        return jsonify({'error': 'Failed to add related item'}), 400

    return jsonify(item), 201

# GET related vet records
@visit_bp.route('/<int:id>/vets', methods=['GET'])
def get_vets(id):
    items, errors = service.get_vets(id)

    # El servicio retorna (None, { 'error': ... }) si no encuentra la entidad padre
    if errors:
        # Podrías chequear si es "not found" u otro tipo de error
        if errors.get('error') == 'Visit not found':
            return jsonify(errors), 404
        # Si fuera un error distinto
        return jsonify({'errors': errors}), 400

    if items is None:
        # Por convención, si items es None pero no hay errors,
        # podrías devolver un 404 o 400 según tu criterio
        return jsonify({'error': 'Failed to fetch related items'}), 400

    return jsonify(items), 200

# POST to add a related vet
@visit_bp.route('/<int:id>/vets', methods=['POST'])

def add_vet(id):
    data = request.get_json()
    item, errors = service.add_vet(id, data)

    if errors:
        # Si errors no es None, puede ser validación o "no se encontró el padre"
        if errors.get('error') == 'Visit not found':
            return jsonify(errors), 404
        # Si son errores de validación u otros
        return jsonify({'errors': errors}), 400

    if not item:
        # Si no existe item y no hay errors, podría ser un error genérico
        return jsonify({'error': 'Failed to add related item'}), 400

    return jsonify(item), 201
