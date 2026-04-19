from flask import Blueprint, request, jsonify
from app.services.libemax.libemax_dipendente_service import LibemaxDipendenteService
from app.auth.decorators import requires_auth

libemax_dipendenti_bp = Blueprint("libemax_dipendenti", __name__, url_prefix="/api/libemax/dipendenti")
_service = LibemaxDipendenteService()


@libemax_dipendenti_bp.route("", methods=["GET"])
@requires_auth
def list_dipendenti():
    result = _service.get_list()
    return jsonify(result)


@libemax_dipendenti_bp.route("", methods=["POST"])
@requires_auth
def sync_dipendente():
    data = request.get_json()
    result = _service.sync(data)
    return jsonify(result), 200


@libemax_dipendenti_bp.route("/<identifier>", methods=["DELETE"])
@requires_auth
def delete_dipendente(identifier):
    by_id = request.args.get("by") == "id"
    _service.delete(identifier, by_id=by_id)
    return jsonify({"success": True})
