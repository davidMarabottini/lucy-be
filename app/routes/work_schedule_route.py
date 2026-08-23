from flask import Blueprint, request, jsonify
from ..services.work_schedule_service import WorkScheduleService
from app.auth.decorators import requires_auth

schedule_bp = Blueprint('work_schedules', __name__, url_prefix='/api/work-schedules')

@schedule_bp.route('', methods=['GET'])
# @requires_auth
def get_work_schedules():
    schedules = WorkScheduleService.get_all()
    return jsonify(schedules), 200

@schedule_bp.route('/<int:id>', methods=['GET'])
# @requires_auth
def get_one(id):
    schedule = WorkScheduleService.get_by_id(id)
    if not schedule:
        return jsonify({"message": "Orario non trovato"}), 404
    return jsonify(schedule.to_dict())

@schedule_bp.route('/contract/<int:contract_id>', methods=['GET'])
# @requires_auth
def get_by_contract(contract_id):
    schedules = WorkScheduleService.get_by_contract(contract_id)
    return jsonify([s.to_dict() for s in schedules]), 200

@schedule_bp.route('', methods=['POST'])
# @requires_auth
def create():
    try:
        schedule = WorkScheduleService.create(request.json)
        full_schedule = WorkScheduleService.get_by_id(schedule.id)
        return jsonify(full_schedule.to_dict()), 201
    except Exception as e:
        return jsonify({"message": str(e)}), 400

@schedule_bp.route('/<int:id>', methods=['PUT'])
# @requires_auth
def update(id):
    try:
        schedule = WorkScheduleService.update(id, request.json)
        if not schedule:
            return jsonify({"message": "Orario non trovato"}), 404
        return jsonify(schedule.to_dict())
    except Exception as e:
        return jsonify({"message": str(e)}), 400

@schedule_bp.route('/<int:id>', methods=['DELETE'])
# @requires_auth
def delete(id):
    if WorkScheduleService.delete(id):
        return jsonify({"message": "Eliminato con successo"}), 200
    return jsonify({"message": "Orario non trovato"}), 404

@schedule_bp.route('/bulk-update', methods=['PUT'])
# @requires_auth
def bulk_update():
    try:
        data = request.json
        if not isinstance(data, list):
            return jsonify({"message": "Payload non valido: atteso un array di elementi"}), 400
            
        updated_schedules = WorkScheduleService.bulk_update(data)
        return jsonify([s.to_dict() for s in updated_schedules]), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 400

@schedule_bp.route('/contract/<int:contract_id>/sync', methods=['POST', 'PUT'])
# @requires_auth
def sync_schedules(contract_id):
    try:
        data = request.get_json(silent=True) or {}
        
        if not isinstance(data, dict):
            return jsonify({"message": "Payload non valido: atteso un oggetto JSON"}), 400

        updated_schedules = WorkScheduleService.sync_contract_schedules(
            contract_id=contract_id,
            payload=data
        )
        return jsonify([s.to_dict() for s in updated_schedules]), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 400