from flask import Blueprint, request, jsonify
from app.services.libemax.libemax_orario_service import LibemaxOrarioService
from app.auth.decorators import requires_auth

libemax_orario_bp = Blueprint("libemax_orario", __name__, url_prefix="/api/libemax/orario-lavorativo")
_service = LibemaxOrarioService()


@libemax_orario_bp.route("", methods=["PUT"])
@requires_auth
def sync_orario():
    data = request.get_json()
    _service.sync(data)
    return jsonify({"success": True}), 200
