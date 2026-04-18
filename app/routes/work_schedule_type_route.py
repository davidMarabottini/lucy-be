from flask import Blueprint, request, jsonify
from ..services.work_schedule_type_service import WorkScheduleTypeService
from ..auth.decorators import requires_auth

wst_bp = Blueprint('work_schedule_types', __name__, url_prefix="/api/work-schedule-types")

@wst_bp.route('', methods=['GET'])
# @requires_auth
def get_types():
    types = WorkScheduleTypeService.get_all()
    return jsonify(types), 200

@wst_bp.route('/<int:wst_id>', methods=['GET'])
# @requires_auth
def get_type(wst_id):
    t = WorkScheduleTypeService.get_by_id(wst_id)
    if not t:
        return jsonify({"error": "Tipologia non trovata"}), 404
    return jsonify(t.to_dict()), 200

@wst_bp.route('', methods=['POST'])
# @requires_auth
def create_type():
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({"error": "Il nome è obbligatorio"}), 400
    
    new_type = WorkScheduleTypeService.create(data)
    return jsonify({"id": new_type.id, "name": new_type.name}), 201

@wst_bp.route('/<int:wst_id>', methods=['PUT'])
# @requires_auth
def update_type(wst_id):
    data = request.get_json()
    updated = WorkScheduleTypeService.update(wst_id, data)
    if not updated:
        return jsonify({"error": "Tipologia non trovata"}), 404
    return jsonify({"message": "Tipologia aggiornata con successo"}), 200

@wst_bp.route('/<int:wst_id>', methods=['DELETE'])
# @requires_auth
def delete_type(wst_id):
    success = WorkScheduleTypeService.delete(wst_id)
    if not success:
        return jsonify({"error": "Tipologia non trovata"}), 404
    return jsonify({"message": "Tipologia eliminata con successo"}), 200