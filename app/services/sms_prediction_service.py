import joblib
import logging
from typing import Optional
from ..utils.preprocessor import TextPreprocessor 

logger = logging.getLogger(__name__)

class SmsPredictionService:
    """Servizio dedicato alla logica di previsione per gli SMS."""
    
    def __init__(self, model_path: str):
        self.model_path = model_path
        self.pipeline = None  # lazy load

    def _load_pipeline(self):
        if self.pipeline is None:
            try:
                self.pipeline = joblib.load(self.model_path)
                logger.info("Pipeline SMS caricata da %s", self.model_path)
            except Exception as e:
                logger.exception("Impossibile caricare pipeline SMS")
                raise FileNotFoundError(f"Impossibile caricare il modello SMS da {self.model_path}: {e}") from e
        
    def predict(self, input_text: str) -> dict:
        """Esegue la classificazione e restituisce il risultato."""
        if not isinstance(input_text, str):
            raise ValueError("input_text deve essere una stringa.")
        self._load_pipeline()
        input_list = [input_text]
        probabilities = self.pipeline.predict_proba(input_list)
        prob_spam = float(probabilities[0][1])
        prediction = int(self.pipeline.predict(input_list)[0])
        result = 'spam' if prediction == 1 else 'ham'
        return {
            'prediction': result,
            'probability_spam': round(prob_spam, 4)
        }
