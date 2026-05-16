from flask import Blueprint, request, jsonify
from app.services.libemax.libemax_documento_service import LibemaxDocumentoService
from app.auth.decorators import requires_auth

libemax_documenti_bp = Blueprint("libemax_documenti", __name__, url_prefix="/api/libemax/documenti")
_service = LibemaxDocumentoService()


@libemax_documenti_bp.route("", methods=["GET"])
@requires_auth
def list_documenti():
    da = request.args.get("from")
    a = request.args.get("to")
    if not da or not a:
        return jsonify({"error": "Parametri 'from' e 'to' obbligatori"}), 400

    filters = {}
    if request.args.get("employee_id"):
        filters["employee_id"] = request.args.get("employee_id", type=int)

    result = _service.get_list(da, a, **filters)
    return jsonify(result)


@libemax_documenti_bp.route("", methods=["POST"])
@requires_auth
def sync_documento():
    data = request.form.to_dict()
    file = request.files.get("document")
    file_tuple = (file.filename, file.stream, file.content_type) if file else None
    result = _service.sync(data, file_tuple=file_tuple)
    return jsonify(result), 200


@libemax_documenti_bp.route("/<code>", methods=["DELETE"])
@requires_auth
def delete_documento(code):
    _service.delete(code)
    return jsonify({"success": True})
