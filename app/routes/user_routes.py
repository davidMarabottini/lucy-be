from flask import Blueprint, jsonify, request

from app.services.user_service import UserService
# from ..services.domain_service import DomainService
from app.utils.exporters import resolve_export_format
from ..auth.decorators import requires_auth

users_bp = Blueprint("users", __name__, url_prefix="/api/users")

@users_bp.route('/export', methods=['GET'])
# @requires_auth
def export_users():
    try:
        return UserService.export(fmt=resolve_export_format())
    except ValueError as e:
        return jsonify({"status": "error", "message": str(e)}), 400

from flask import jsonify, Response
from typing import Tuple, Dict, Any

from flask import jsonify, Response
from typing import Tuple, Dict, Any

@users_bp.route('', methods=['GET'])
def list_users() -> Tuple[Response, int]:
    paginated_data: Dict[str, Any] = UserService.get_all()
    
    user_list_refined = [{
        "id": u.get("id"),
        "username": u.get("username"),
        "email": u.get("email"),
        "name": u.get("name"),
        "surname": u.get("surname"),
        "roles": u.get("roles", []) 
    } for u in paginated_data.get("items", [])]
    
    response_payload = {
        **paginated_data, 
        "items": user_list_refined
    }
    
    return jsonify(response_payload), 200

@users_bp.route('', methods=['POST'])
def add_user():
    data = request.get_json()
    data['roles'] = ['user'] 
    user, error = UserService.create(data)
    
    if error:
        return jsonify({"status": "error", "message": error}), 400
    
    return jsonify({"status": "success", "id": user.id, "message": "OK"}), 201

@users_bp.route('/<int:user_id>', methods=['GET'])
# @requires_auth
def get_single_user(user_id):
    user = UserService.get_by_id(user_id)
    if not user:
        return jsonify({"status": "error", "message": "Utente non trovato"}), 404
    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "name": user.name,
        "surname": user.surname,
        "roles": [r.name for r in user.roles]
    })

@users_bp.route('/<int:user_id>', methods=['PUT'])
# @requires_auth
def update_user(user_id):
    data = request.get_json()
    user, error = UserService.update(user_id, data)
    if error:
        return jsonify({"status": "error", "message": error}), 400
    return jsonify({"status": "success", "message": "Utente aggiornato"})

@users_bp.route('/<int:user_id>', methods=['DELETE'])
# @requires_auth
def delete_user(user_id):
    success = UserService.delete(user_id)
    if not success:
        return jsonify({"status": "error", "message": "Utente non trovato"}), 404
    return jsonify({"status": "success", "message": "Utente eliminato"})
