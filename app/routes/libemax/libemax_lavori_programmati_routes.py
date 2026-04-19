from flask import Blueprint, request, jsonify
from app.services.libemax.libemax_lavoro_programmato_service import LibemaxLavoroProgrammatoService
from app.auth.decorators import requires_auth

libemax_lavori_programmati_bp = Blueprint("libemax_lavori_programmati", __name__, url_prefix="/api/libemax/lavori-programmati")
_service = LibemaxLavoroProgrammatoService()


@libemax_lavori_programmati_bp.route("", methods=["GET"])
@requires_auth
def list_lavori_programmati():
    da = request.args.get("from")
    a = request.args.get("to")
    if not da or not a:
        return jsonify({"error": "Parametri 'from' e 'to' obbligatori"}), 400

    filters = {}
    if request.args.get("employee_id"):
        filters["employee_id"] = request.args.get("employee_id", type=int)

    result = _service.get_list(da, a, **filters)
    return jsonify(result)


@libemax_lavori_programmati_bp.route("", methods=["POST"])
@requires_auth
def sync_lavoro_programmato():
    data = request.get_json()
    result = _service.sync(data)
    return jsonify(result), 200


@libemax_lavori_programmati_bp.route("/<code>", methods=["DELETE"])
@requires_auth
def delete_lavoro_programmato(code):
    _service.delete(code)
    return jsonify({"success": True})
