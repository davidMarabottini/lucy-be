from flask import Blueprint, request, jsonify, g
from sklearn import logger

from app.exception import APIError
from flask import current_app
from ..auth.decorators import requires_auth

predict_bp = Blueprint("predict", __name__, url_prefix="/predict")


@predict_bp.route('/<model_type>', methods=['POST'])
@requires_auth
def predict_dynamic(model_type):
    raw_text = request.values.get('text')
    if raw_text is None:
        json_body = request.get_json(silent=True) or {}
        raw_text = json_body.get('text')

    input_text = raw_text.strip() if isinstance(raw_text, str) else None
    logger.info("Received prediction request for model '%s' with text: %s", model_type, input_text)

    if not input_text:
        raise APIError('Parametro "text" mancante nella query string o body.', status_code=400)

    try:
        prediction_service = current_app.model_registry.get_model(model_type)
    except ValueError as e:
        raise APIError(str(e), status_code=404)

    try:
        results = prediction_service.predict(input_text)
    except Exception as exc:
        logger.exception("Errore durante la previsione")
        raise APIError("Errore interno durante la previsione.", status_code=500) from exc

    return jsonify({
        'status': 'success',
        'model_used': model_type,
        'input_text': input_text,
        **results
    })
