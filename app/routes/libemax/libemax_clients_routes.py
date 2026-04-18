from flask import Blueprint, jsonify, current_app
from ...services.libemax.libemax_client_service import LibemaxClientService
from app.auth.decorators import requires_auth
import logging

logging.info("Creazione blueprint libemax_clients")
libemax_clients_bp = Blueprint("libemax_clients", __name__, url_prefix="/api/libemax/clients")
# Lazy initialization del service se preferisci, o istanza globale
_service = None

def get_service():
    global _service
    logging.info("Lancio get_service")

    if _service is None:
      logging.info("_service vuoto, inizializzazione")
      _service = LibemaxClientService()
    return _service

@libemax_clients_bp.route("/sync", methods=["POST"])
# @requires_auth
def sync_libemax_clients():
  logging.info("Inizializzazione service")
  service = get_service()
  logging.info("service inizializzato")
  count, error = service.sync_clients()
  
  if error:
    logging.error(f"Errore {error}")
    current_app.logger.error(f"Sync failed: {error}")
    return jsonify({"status": "error", "message": error}), 500
  
  logging.info("Libemax sincronizzato")
  return jsonify({
      "status": "success", 
      "synced_count": count
  }), 200