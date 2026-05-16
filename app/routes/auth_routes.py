from flask import Blueprint, request, jsonify, g
from ..services.auth_service import AuthService
from ..auth.decorators import requires_auth
from ..services.user_service import UserService

auth_bp = Blueprint("auth", __name__, url_prefix="")

@auth_bp.route('/api/login', methods=['POST'])
def login():
  data = request.get_json()
  response, error = AuthService.login_user(data.get('username'), data.get('password'))
  
  if error:
      return jsonify({"status": "error", "message": error}), 401
  return response

@auth_bp.route('/api/logout', methods=['POST'])
def logout():
  return AuthService.logout_user()

@auth_bp.route('/api/me', methods=['GET'])
@requires_auth
def me():
  user = g.current_user
  return jsonify({
      "id": user.id,
      "user": user.username,
      "role": [r.name for r in user.roles]
  })

@auth_bp.route('/api/users/me', methods=['GET'])
@requires_auth
def get_me():
  user = g.current_user
  return jsonify({
      "id": user.id,
      "username": user.username,
      "email": user.email,
      "gender": user.gender,
      "name": user.name,
      "surname": user.surname,
      "roles": [r.name for r in user.roles]
  })

@auth_bp.route('/api/users/me', methods=['PUT'])
@requires_auth
def update_me():
  user = g.current_user
  data = request.get_json()

  updated_user, error = UserService.update(user.id, data)

  if error:
      return jsonify({"status": "error", "message": error}), 400

  return jsonify({
      "status": "success",
      "user": {
          "id": updated_user.id,
          "username": updated_user.username,
          "email": updated_user.email,
          "gender": user.gender,
          "name": updated_user.name,
          "surname": updated_user.surname,
          "roles": [r.name for r in updated_user.roles]
      }
  })

@auth_bp.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'}), 200