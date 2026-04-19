from flask import Blueprint, request, jsonify
from app.services.libemax.libemax_produttivita_service import LibemaxProduttivitaService
from app.auth.decorators import requires_auth

libemax_produttivita_bp = Blueprint("libemax_produttivita", __name__, url_prefix="/api/libemax/produttivita")
_service = LibemaxProduttivitaService()


@libemax_produttivita_bp.route("", methods=["GET"])
@requires_auth
def list_produttivita():
    result = _service.get_list()
    return jsonify(result)


@libemax_produttivita_bp.route("", methods=["POST"])
@requires_auth
def sync_produttivita():
    data = request.get_json()
    result = _service.sync(data)
    return jsonify(result), 200


@libemax_produttivita_bp.route("/<code>", methods=["DELETE"])
@requires_auth
def delete_produttivita(code):
    _service.delete(code)
    return jsonify({"success": True})
