import os
import logging
from pathlib import Path
import threading
from .sms_prediction_service import SmsPredictionService 
from .mail_prediction_service import MailPredictionService 

logger = logging.getLogger(__name__)

class ModelRegistry:
    """
    Gestisce il caricamento e l'accesso dinamico ai diversi servizi di previsione.
    Caricamento lazy e thread-safe.
    """
    def __init__(self, root_dir: str):
        self.root_dir = Path(root_dir)
        self._models = {}
        self._model_paths = {}
        self._lock = threading.Lock()
        self._discover_models()

    def _discover_models(self):
        sms_model = self.root_dir.joinpath('..', 'models', 'sms_spam_pipeline.joblib').resolve()
        mail_model = self.root_dir.joinpath('..', 'models', 'mail_spam_pipeline.joblib').resolve()

        self._model_paths['sms'] = (SmsPredictionService, str(sms_model))
        self._models['sms'] = None
        self._model_paths['mail'] = (MailPredictionService, str(mail_model))
        self._models['mail'] = None

    def _load_model(self, model_type: str):
        with self._lock:
            if self._models.get(model_type):
                return self._models[model_type]
            if model_type not in self._model_paths:
                raise ValueError(f"Tipo di modello '{model_type}' non registrato.")
            service_cls, path = self._model_paths[model_type]
            if not Path(path).exists():
                raise FileNotFoundError(f"Modello non trovato: {path}")
            instance = service_cls(model_path=path)
            self._models[model_type] = instance
            logger.info("Modello '%s' caricato da %s", model_type, path)
            return instance

    def get_model(self, model_type: str):
        if model_type not in self._models:
            raise ValueError(f"Tipo di modello '{model_type}' non registrato.")
        if self._models[model_type] is None:
            return self._load_model(model_type)
        return self._models[model_type]