from flask import Blueprint, request, jsonify
from app.services.libemax.libemax_attivita_service import LibemaxAttivitaService
from app.auth.decorators import requires_auth

libemax_attivita_bp = Blueprint("libemax_attivita", __name__, url_prefix="/api/libemax/attivita")
_service = LibemaxAttivitaService()


@libemax_attivita_bp.route("", methods=["GET"])
@requires_auth
def list_attivita():
    result = _service.get_list()
    return jsonify(result)


@libemax_attivita_bp.route("", methods=["POST"])
@requires_auth
def sync_attivita():
    data = request.get_json()
    result = _service.sync(data)
    return jsonify(result), 200


@libemax_attivita_bp.route("/<code>", methods=["DELETE"])
@requires_auth
def delete_attivita(code):
    _service.delete(code)
    return jsonify({"success": True})
