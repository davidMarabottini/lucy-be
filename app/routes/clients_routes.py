from flask import Blueprint, request, jsonify
from app.services.client_service import ClientService

clients_bp = Blueprint("clients", __name__, url_prefix="/api/clients")

@clients_bp.route("", methods=["GET"])
def list_clients():
    clients = ClientService.get_all()
    return jsonify(clients), 200


@clients_bp.route("/<int:client_id>", methods=["GET"])
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
def create_client():
    data = request.get_json()
    client = ClientService.create(data)
    return jsonify({"id": client.id}), 201

@clients_bp.route("/<int:client_id>", methods=["DELETE"])
def delete_client(client_id):
    isDeleted = ClientService.delete(client_id)
    return jsonify({"success": isDeleted})
    