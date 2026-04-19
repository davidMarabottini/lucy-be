from flask import Blueprint, request, jsonify
from app.services.libemax.libemax_foglio_presenze_service import LibemaxFoglioPresenzeService
from app.auth.decorators import requires_auth

libemax_foglio_presenze_bp = Blueprint("libemax_foglio_presenze", __name__, url_prefix="/api/libemax/foglio-presenze")
_service = LibemaxFoglioPresenzeService()


@libemax_foglio_presenze_bp.route("", methods=["GET"])
@requires_auth
def list_foglio_presenze():
    year = request.args.get("year")
    month = request.args.get("month")
    rounding = request.args.get("rounding", type=int)
    format_type = request.args.get("format", type=int)

    if not all([year, month, rounding is not None, format_type is not None]):
        return jsonify({"error": "Parametri 'year', 'month', 'rounding' e 'format' obbligatori"}), 400

    filters = {}
    if request.args.get("only_with_code"):
        filters["only_with_code"] = request.args["only_with_code"]
    if request.args.get("employee_code"):
        filters["employee_code"] = request.args["employee_code"]

    result = _service.get_list(year, month, rounding, format_type, **filters)
    return jsonify(result)
