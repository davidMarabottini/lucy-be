import joblib
from ..utils.rawEmailToFeaturesTransformer import RawEmailToFeaturesTransformer 

class MailPredictionService:
    """Servizio dedicato alla logica di previsione per le mail."""
    
    def __init__(self, model_path: str):
        self.pipeline = joblib.load(model_path)
        
    def predict(self, input_text: str) -> dict:
        """Esegue la classificazione e restituisce il risultato."""
        
        input_list = [input_text]
        
        probabilities = self.pipeline.predict_proba(input_list)
        prob_spam = probabilities[0][1]
        prediction = self.pipeline.predict(input_list)[0]
        result = 'spam' if prediction == 1 else 'ham'

        return {
            'prediction': result,
            'probability_spam': round(prob_spam, 4)
        }
