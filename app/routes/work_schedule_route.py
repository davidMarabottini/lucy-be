from flask import Blueprint, request, jsonify
from ..services.work_schedule_service import WorkScheduleService
from app.auth.decorators  import paginated_response, requires_auth

schedule_bp = Blueprint('work_schedules', __name__, url_prefix='/api/work-schedules')

@schedule_bp.route('', methods=['GET'])
@requires_auth
@paginated_response
def get_work_schedules():
    return WorkScheduleService.get_all_schedules_query()

@schedule_bp.route('/<int:id>', methods=['GET'])
@requires_auth
def get_one(id):
    schedule = WorkScheduleService.get_by_id(id)
    if not schedule:
        return jsonify({"message": "Orario non trovato"}), 404
    return jsonify(schedule.to_dict())

@schedule_bp.route('', methods=['POST'])
@requires_auth
def create():
    try:
        schedule = WorkScheduleService.create_schedule(request.json)
        # Recupero l'oggetto completo di join per la risposta
        full_schedule = WorkScheduleService.get_by_id(schedule.id)
        return jsonify(full_schedule.to_dict()), 201
    except Exception as e:
        return jsonify({"message": str(e)}), 400

@schedule_bp.route('/<int:id>', methods=['PUT'])
@requires_auth
def update(id):
    try:
        schedule = WorkScheduleService.update_schedule(id, request.json)
        if not schedule:
            return jsonify({"message": "Orario non trovato"}), 404
        return jsonify(schedule.to_dict())
    except Exception as e:
        return jsonify({"message": str(e)}), 400

@schedule_bp.route('/<int:id>', methods=['DELETE'])
@requires_auth
def delete(id):
    if WorkScheduleService.delete_schedule(id):
        return jsonify({"message": "Eliminato con successo"}), 200
    return jsonify({"message": "Orario non trovato"}), 404