from flask import Blueprint, request, jsonify
from app.services.libemax.libemax_accesso_service import LibemaxAccessoService
from app.auth.decorators import requires_auth

libemax_accessi_bp = Blueprint("libemax_accessi", __name__, url_prefix="/api/libemax/accessi")
_service = LibemaxAccessoService()


@libemax_accessi_bp.route("", methods=["GET"])
@requires_auth
def list_accessi():
    result = _service.get_list()
    return jsonify(result)


@libemax_accessi_bp.route("", methods=["POST"])
@requires_auth
def sync_accesso():
    data = request.get_json()
    _service.sync(data)
    return jsonify({"success": True}), 200


@libemax_accessi_bp.route("/<identifier>", methods=["DELETE"])
@requires_auth
def delete_accesso(identifier):
    by_id = request.args.get("by") == "id"
    _service.delete(identifier, by_id=by_id)
    return jsonify({"success": True})
