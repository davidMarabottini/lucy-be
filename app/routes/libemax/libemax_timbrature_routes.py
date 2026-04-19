from flask import Blueprint, request, jsonify
from app.services.libemax.libemax_timbratura_service import LibemaxTimbraturaService
from app.auth.decorators import requires_auth

libemax_timbrature_bp = Blueprint("libemax_timbrature", __name__, url_prefix="/api/libemax/timbrature")
_service = LibemaxTimbraturaService()


@libemax_timbrature_bp.route("", methods=["GET"])
@requires_auth
def list_timbrature():
    da = request.args.get("from")
    a = request.args.get("to")
    if not da or not a:
        return jsonify({"error": "Parametri 'from' e 'to' obbligatori"}), 400

    filters = {}
    if request.args.get("last_modified_from"):
        filters["last_modified_from"] = request.args["last_modified_from"]
    if request.args.get("last_modified_to"):
        filters["last_modified_to"] = request.args["last_modified_to"]
    if request.args.get("type"):
        filters["type"] = request.args["type"]
    if request.args.get("employee_code"):
        filters["employee_code"] = request.args["employee_code"]
    if request.args.get("client_code"):
        filters["client_code"] = request.args["client_code"]
    if request.args.get("activity_code"):
        filters["activity_code"] = request.args["activity_code"]
    if request.args.get("only_with_code"):
        filters["only_with_code"] = request.args["only_with_code"]
    if request.args.get("format"):
        filters["format"] = request.args["format"]

    result = _service.get_list(da, a, **filters)
    return jsonify(result)
