from flask import Blueprint, request, jsonify
from app.services.libemax.libemax_indennita_service import LibemaxIndennitaService
from app.auth.decorators import requires_auth

libemax_indennita_bp = Blueprint("libemax_indennita", __name__, url_prefix="/api/libemax/indennita")
_service = LibemaxIndennitaService()


@libemax_indennita_bp.route("", methods=["GET"])
@requires_auth
def list_indennita():
    da = request.args.get("from")
    a = request.args.get("to")
    if not da or not a:
        return jsonify({"error": "Parametri 'from' e 'to' obbligatori"}), 400

    filters = {}
    if request.args.get("status") is not None:
        filters["status"] = request.args.get("status", type=int)
    if request.args.get("reimbursed") is not None:
        filters["reimbursed"] = request.args.get("reimbursed", type=int)

    result = _service.get_list(da, a, **filters)
    return jsonify(result)


@libemax_indennita_bp.route("/types", methods=["GET"])
@requires_auth
def list_indennita_types():
    result = _service.get_types()
    return jsonify(result)
