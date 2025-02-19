from flask import Blueprint, request, jsonify
from app.services.vet_service import VetService


vet_bp = Blueprint('vet_bp', __name__)
service = VetService()

# GET all records
@vet_bp.route('/', methods=['GET'])

def get_all_vets():
    items = service.get_all()  # Este m�todo devuelve s�lo la lista (sin errores)
    return jsonify(items), 200

# GET a single record by ID
@vet_bp.route('/<int:id>', methods=['GET'])

def get_vet(id):
    item = service.get_by_id(id)  # Este m�todo tambi�n devuelve s�lo el objeto o None
    if not item:
        return jsonify({'error': 'Vet not found'}), 404
    return jsonify(item), 200

# POST to create a new record
@vet_bp.route('/', methods=['POST'])

def create_vet():
    data = request.get_json()
    item, errors = service.create(data)
    if errors:
        # Si hay errores, normalmente son de validaci�n
        return jsonify({'errors': errors}), 400
    # item es el dict ya serializado desde el servicio
    return jsonify(item), 201

# PUT to update an existing record
@vet_bp.route('/<int:id>', methods=['PUT'])

def update_vet(id):
    data = request.get_json()
    item, errors = service.update(id, data)

    if errors:
        # Si hay errores, pueden ser de validaci�n o alg�n otro
        return jsonify({'errors': errors}), 400

    if not item:
        # Puede que el servicio retorne (None, None) si no existe la entidad
        return jsonify({'error': 'Vet not found'}), 404

    return jsonify(item), 200

# DELETE to remove a record
@vet_bp.route('/<int:id>', methods=['DELETE'])

def delete_vet(id):
    success = service.delete(id)  # Devuelve True o False
    if not success:
        return jsonify({'error': 'Vet not found'}), 404
    return '', 204


# GET related visits records
@vet_bp.route('/<int:id>/visits', methods=['GET'])
def get_visitss(id):
    items, errors = service.get_visitss(id)

    # El servicio retorna (None, { 'error': ... }) si no encuentra la entidad padre
    if errors:
        # Podr�as chequear si es "not found" u otro tipo de error
        if errors.get('error') == 'Vet not found':
            return jsonify(errors), 404
        # Si fuera un error distinto
        return jsonify({'errors': errors}), 400

    if items is None:
        # Por convenci�n, si items es None pero no hay errors,
        # podr�as devolver un 404 o 400 seg�n tu criterio
        return jsonify({'error': 'Failed to fetch related items'}), 400

    return jsonify(items), 200

# POST to add a related visit
@vet_bp.route('/<int:id>/visits', methods=['POST'])

def add_visits(id):
    data = request.get_json()
    item, errors = service.add_visits(id, data)

    if errors:
        # Si errors no es None, puede ser validaci�n o "no se encontr� el padre"
        if errors.get('error') == 'Vet not found':
            return jsonify(errors), 404
        # Si son errores de validaci�n u otros
        return jsonify({'errors': errors}), 400

    if not item:
        # Si no existe item y no hay errors, podr�a ser un error gen�rico
        return jsonify({'error': 'Failed to add related item'}), 400

    return jsonify(item), 201
