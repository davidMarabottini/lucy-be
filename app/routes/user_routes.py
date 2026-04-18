from flask import Blueprint, jsonify, request

from app.services.user_service import UserService
# from ..services.domain_service import DomainService
from ..auth.decorators import requires_auth

users_bp = Blueprint("users", __name__, url_prefix="/api/users")

@users_bp.route('', methods=['GET'])
# @requires_auth
def list_users():
    users = UserService.get_all()
    return jsonify([{
        "id": u.id,
        "username": u.username,
        "email": u.email,
        "name": u.name,
        "surname": u.surname,
        "roles": [r.name for r in u.roles]
    } for u in users])

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
