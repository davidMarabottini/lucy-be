from flask import Blueprint, request, jsonify
from app.services.work_activity_service import WorkActivityService
from ..auth.decorators import requires_auth

activities_bp = Blueprint("activities", __name__, url_prefix="/api/activities")

@activities_bp.route("", methods=["GET"])
@requires_auth
def list_activities():
    """Ritorna l'anagrafica di tutte le attività (es. Pulizie, Portineria)"""
    activities = WorkActivityService.get_all()
    # Usa to_dict() che abbiamo aggiunto nel modello
    return jsonify(activities)

@activities_bp.route("", methods=["POST"])
@requires_auth
def create_activity():
    """Crea un nuovo tipo di attività nel catalogo"""
    data = request.get_json()
    
    # Validazione minima: name è obbligatorio nel nuovo modello
    if not data or 'name' not in data:
        return jsonify({"error": "Il campo 'name' è obbligatorio"}), 400
        
    activity = WorkActivityService.create(data)
    # Restituiamo l'oggetto completo così il frontend può aggiornare la lista subito
    return jsonify(activity.to_dict()), 201

@activities_bp.route("/<int:activity_id>", methods=["GET"])
@requires_auth
def get_activity(activity_id):
    activity = WorkActivityService.get_by_id(activity_id)
    if not activity:
        return jsonify({"error": "Attività non trovata"}), 404
    return jsonify(activity.to_dict())

@activities_bp.route("/<int:activity_id>", methods=["PUT"])
@requires_auth
def update_activity(activity_id):
    """Aggiorna name o description di un'attività esistente"""
    data = request.get_json()
    activity = WorkActivityService.update(activity_id, data)
    
    if not activity:
        return jsonify({"error": "Attività non trovata"}), 404
        
    return jsonify({
        "status": "success",
        "message": "Attività aggiornata",
        "data": activity.to_dict()
    })

@activities_bp.route("/<int:activity_id>", methods=["DELETE"])
@requires_auth
def delete_activity(activity_id):
    success = WorkActivityService.delete(activity_id)
    if not success:
        return jsonify({"error": "Attività non trovata"}), 404
        
    return jsonify({
        "status": "success", 
        "message": "Attività eliminata correttamente"
    })