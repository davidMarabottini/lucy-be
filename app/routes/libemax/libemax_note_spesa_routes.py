from flask import Blueprint, request, jsonify
from app.services.libemax.libemax_nota_spesa_service import LibemaxNotaSpesaService
from app.auth.decorators import requires_auth

libemax_note_spesa_bp = Blueprint("libemax_note_spesa", __name__, url_prefix="/api/libemax/note-spesa")
_service = LibemaxNotaSpesaService()


@libemax_note_spesa_bp.route("", methods=["GET"])
@requires_auth
def list_note_spesa():
    da = request.args.get("from")
    a = request.args.get("to")
    if not da or not a:
        return jsonify({"error": "Parametri 'from' e 'to' obbligatori"}), 400

    filters = {}
    if request.args.get("approved") is not None:
        filters["approved"] = request.args.get("approved", type=int)

    result = _service.get_list(da, a, **filters)
    return jsonify(result)
