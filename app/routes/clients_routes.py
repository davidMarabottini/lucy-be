from flask import Blueprint, request, jsonify
from app.services.client_service import ClientService
from ..auth.decorators import requires_auth

clients_bp = Blueprint("clients", __name__, url_prefix="/api/clients")

@clients_bp.route("", methods=["GET"])
@requires_auth
def list_clients():
    clients = ClientService.get_all()
    return jsonify(clients), 200


@clients_bp.route("/<int:client_id>", methods=["GET"])
@requires_auth
def get_client(client_id):
    client = ClientService.get_by_id(client_id)
    if not client:
        return jsonify({"error": "Not found"}), 404

    return jsonify({
        "id": client.id,
        "name": client.name,
        "email": client.email,
        "phone": client.phone
    })

@clients_bp.route("", methods=["POST"])
@requires_auth
def create_client():
    data = request.get_json()
    client = ClientService.create(data)
    return jsonify({"id": client.id}), 201

@clients_bp.route("/<int:client_id>", methods=["DELETE"])
@requires_auth
def delete_client(client_id):
    isDeleted = ClientService.delete(client_id)
    return jsonify({"success": isDeleted})
    