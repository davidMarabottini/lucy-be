from flask import jsonify
import logging

logger = logging.getLogger(__name__)

class APIError(Exception):
    def __init__(self, message: str, status_code: int = 500):
        super().__init__(message)
        self.message = message
        self.status_code = status_code

def register_error_handlers(app):
    @app.errorhandler(APIError)
    def handle_api_error(error):
        logger.warning("APIError: %s", error.message)
        response = jsonify({'error': error.message})
        return response, error.status_code

    @app.errorhandler(404)
    def handle_404(error):
        return jsonify({'error': 'Endpoint non trovato.'}), 404

    @app.errorhandler(Exception)
    def handle_exception(error):
        logger.exception("Unhandled exception")
        return jsonify({'error': 'Errore interno del server.'}), 500
