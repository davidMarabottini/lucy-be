from flask import Blueprint, request, jsonify
from app.services.libemax.libemax_scansione_service import LibemaxScansioneService
from app.auth.decorators import requires_auth

libemax_scansioni_bp = Blueprint("libemax_scansioni", __name__, url_prefix="/api/libemax/scansioni")
_service = LibemaxScansioneService()


@libemax_scansioni_bp.route("", methods=["GET"])
@requires_auth
def list_scansioni():
    filters = {}
    if request.args.get("from_last_scan"):
        filters["from_last_scan"] = request.args["from_last_scan"]

    result = _service.get_list(**filters)
    return jsonify(result)


@libemax_scansioni_bp.route("/<code>", methods=["GET"])
@requires_auth
def get_scansione_detail(code):
    result = _service.get_detail(code)
    return jsonify(result)
