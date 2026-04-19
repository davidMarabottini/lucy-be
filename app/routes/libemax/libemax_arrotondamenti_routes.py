from flask import Blueprint, jsonify
from app.services.libemax.libemax_arrotondamento_service import LibemaxArrotondamentoService
from app.auth.decorators import requires_auth

libemax_arrotondamenti_bp = Blueprint("libemax_arrotondamenti", __name__, url_prefix="/api/libemax/arrotondamenti")
_service = LibemaxArrotondamentoService()


@libemax_arrotondamenti_bp.route("", methods=["GET"])
@requires_auth
def list_arrotondamenti():
    result = _service.get_list()
    return jsonify(result)
