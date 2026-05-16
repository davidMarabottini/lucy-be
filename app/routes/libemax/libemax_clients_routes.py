from flask import Blueprint, jsonify, current_app
from ...services.libemax.libemax_client_service import LibemaxClienteService
from app.auth.decorators import requires_auth
import logging

logging.info("Creazione blueprint libemax_clients")
libemax_clients_bp = Blueprint("libemax_clients", __name__, url_prefix="/api/libemax/clients")

_service = LibemaxClienteService()


@libemax_clients_bp.route("/sync", methods=["POST"])
@requires_auth
def sync_libemax_clients():
    logging.info("Sincronizzazione clienti Libemax")
    result = _service.get_list()
    return jsonify({
        "status": "success",
        "data": result
    }), 200