from flask import Blueprint, request, jsonify
from app.services.pet_service import PetService


pet_bp = Blueprint('pet_bp', __name__)
service = PetService()

# GET all records
@pet_bp.route('/', methods=['GET'])

def get_all_pets():
    items = service.get_all()  # Este método devuelve sólo la lista (sin errores)
    return jsonify(items), 200

# GET a single record by ID
@pet_bp.route('/<int:id>', methods=['GET'])

def get_pet(id):
    item = service.get_by_id(id)  # Este método también devuelve sólo el objeto o None
    if not item:
        return jsonify({'error': 'Pet not found'}), 404
    return jsonify(item), 200

# POST to create a new record
@pet_bp.route('/', methods=['POST'])

def create_pet():
    data = request.get_json()
    item, errors = service.create(data)
    if errors:
        # Si hay errores, normalmente son de validación
        return jsonify({'errors': errors}), 400
    # item es el dict ya serializado desde el servicio
    return jsonify(item), 201

# PUT to update an existing record
@pet_bp.route('/<int:id>', methods=['PUT'])

def update_pet(id):
    data = request.get_json()
    item, errors = service.update(id, data)

    if errors:
        # Si hay errores, pueden ser de validación o algún otro
        return jsonify({'errors': errors}), 400

    if not item:
        # Puede que el servicio retorne (None, None) si no existe la entidad
        return jsonify({'error': 'Pet not found'}), 404

    return jsonify(item), 200

# DELETE to remove a record
@pet_bp.route('/<int:id>', methods=['DELETE'])

def delete_pet(id):
    success = service.delete(id)  # Devuelve True o False
    if not success:
        return jsonify({'error': 'Pet not found'}), 404
    return '', 204


# GET related owner records
@pet_bp.route('/<int:id>/owners', methods=['GET'])
def get_owners(id):
    items, errors = service.get_owners(id)

    # El servicio retorna (None, { 'error': ... }) si no encuentra la entidad padre
    if errors:
        # Podrías chequear si es "not found" u otro tipo de error
        if errors.get('error') == 'Pet not found':
            return jsonify(errors), 404
        # Si fuera un error distinto
        return jsonify({'errors': errors}), 400

    if items is None:
        # Por convención, si items es None pero no hay errors,
        # podrías devolver un 404 o 400 según tu criterio
        return jsonify({'error': 'Failed to fetch related items'}), 400

    return jsonify(items), 200

# POST to add a related owner
@pet_bp.route('/<int:id>/owners', methods=['POST'])

def add_owner(id):
    data = request.get_json()
    item, errors = service.add_owner(id, data)

    if errors:
        # Si errors no es None, puede ser validación o "no se encontró el padre"
        if errors.get('error') == 'Pet not found':
            return jsonify(errors), 404
        # Si son errores de validación u otros
        return jsonify({'errors': errors}), 400

    if not item:
        # Si no existe item y no hay errors, podría ser un error genérico
        return jsonify({'error': 'Failed to add related item'}), 400

    return jsonify(item), 201

# GET related visits records
@pet_bp.route('/<int:id>/visits', methods=['GET'])
def get_visitss(id):
    items, errors = service.get_visitss(id)

    # El servicio retorna (None, { 'error': ... }) si no encuentra la entidad padre
    if errors:
        # Podrías chequear si es "not found" u otro tipo de error
        if errors.get('error') == 'Pet not found':
            return jsonify(errors), 404
        # Si fuera un error distinto
        return jsonify({'errors': errors}), 400

    if items is None:
        # Por convención, si items es None pero no hay errors,
        # podrías devolver un 404 o 400 según tu criterio
        return jsonify({'error': 'Failed to fetch related items'}), 400

    return jsonify(items), 200

# POST to add a related visit
@pet_bp.route('/<int:id>/visits', methods=['POST'])

def add_visits(id):
    data = request.get_json()
    item, errors = service.add_visits(id, data)

    if errors:
        # Si errors no es None, puede ser validación o "no se encontró el padre"
        if errors.get('error') == 'Pet not found':
            return jsonify(errors), 404
        # Si son errores de validación u otros
        return jsonify({'errors': errors}), 400

    if not item:
        # Si no existe item y no hay errors, podría ser un error genérico
        return jsonify({'error': 'Failed to add related item'}), 400

    return jsonify(item), 201
