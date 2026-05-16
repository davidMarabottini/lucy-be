from flask import Blueprint, request, jsonify
from app.services.libemax.libemax_richiesta_service import LibemaxRichiestaService
from app.auth.decorators import requires_auth

libemax_richieste_bp = Blueprint("libemax_richieste", __name__, url_prefix="/api/libemax/richieste")
_service = LibemaxRichiestaService()


@libemax_richieste_bp.route("", methods=["GET"])
@requires_auth
def list_richieste():
    filters = {}
    if request.args.get("from"):
        filters["from"] = request.args["from"]
    if request.args.get("to"):
        filters["to"] = request.args["to"]
    if request.args.get("inserted_from"):
        filters["inserted_from"] = request.args["inserted_from"]
    if request.args.get("inserted_to"):
        filters["inserted_to"] = request.args["inserted_to"]
    if request.args.get("approved") is not None:
        filters["approved"] = request.args.get("approved", type=int)

    has_date_range = filters.get("from") and filters.get("to")
    has_insert_range = filters.get("inserted_from") and filters.get("inserted_to")
    if not has_date_range and not has_insert_range:
        return jsonify({"error": "Almeno una coppia di date obbligatoria: from/to oppure inserted_from/inserted_to"}), 400

    result = _service.get_list(**filters)
    return jsonify(result)


@libemax_richieste_bp.route("/types", methods=["GET"])
@requires_auth
def list_richieste_types():
    result = _service.get_types()
    return jsonify(result)
