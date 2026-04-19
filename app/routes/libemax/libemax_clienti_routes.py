from flask import Blueprint, request, jsonify
from app.services.libemax.libemax_client_service import LibemaxClienteService
from app.auth.decorators import requires_auth

libemax_clienti_bp = Blueprint("libemax_clienti", __name__, url_prefix="/api/libemax/clienti")
_service = LibemaxClienteService()


@libemax_clienti_bp.route("", methods=["GET"])
@requires_auth
def list_clienti():
    result = _service.get_list()
    return jsonify(result)


@libemax_clienti_bp.route("", methods=["POST"])
@requires_auth
def sync_cliente():
    data = request.get_json()
    result = _service.sync(data)
    return jsonify(result), 200


@libemax_clienti_bp.route("/<identifier>", methods=["DELETE"])
@requires_auth
def delete_cliente(identifier):
    by_id = request.args.get("by") == "id"
    _service.delete(identifier, by_id=by_id)
    return jsonify({"success": True})
