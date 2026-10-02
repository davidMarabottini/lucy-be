from flask import Blueprint, request, jsonify
from ..services.store_service import StoreService
from ..utils.exporters import resolve_export_format
from ..auth.decorators import requires_auth

stores_bp = Blueprint('stores_bp', __name__, url_prefix="/api/stores")

@stores_bp.route('', methods=['GET'])
# @requires_auth
def get_stores():
    stores = StoreService.get_all()
    return jsonify(stores), 200

@stores_bp.route('/export', methods=['GET'])
# @requires_auth
def export_stores():
    try:
        return StoreService.export(fmt=resolve_export_format())
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@stores_bp.route('/<int:store_id>', methods=['GET'])
# @requires_auth
def get_store(store_id):
    store = StoreService.get_by_id(store_id)
    if not store:
        return jsonify({"error": "Store non trovato"}), 404
    return jsonify(store.to_dict()), 200

@stores_bp.route('', methods=['POST'])
# @requires_auth
def create_store():
    data = request.get_json()
    missing = [f for f in ('company_id', 'name', 'price') if not data or f not in data]
    if missing:
        return jsonify({"error": f"Campi obbligatori mancanti: {', '.join(missing)}"}), 400

    new_store = StoreService.create(data)
    return jsonify(new_store.to_dict()), 201

@stores_bp.route('/<int:store_id>', methods=['PUT'])
# @requires_auth
def update_store(store_id):
    data = request.get_json()
    updated_store = StoreService.update(store_id, data)
    if not updated_store:
        return jsonify({"error": "Store non trovato"}), 404
    return jsonify(updated_store.to_dict()), 200

@stores_bp.route('/<int:store_id>', methods=['DELETE'])
# @requires_auth
def delete_store(store_id):
    success = StoreService.delete(store_id)
    if not success:
        return jsonify({"error": "Store non trovato"}), 404
    return jsonify({"message": "Store eliminato con successo"}), 200
