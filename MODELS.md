# Modelli — convenzioni e metadata

Struttura raccomandata
- `models/{type}/` (es. `models/sms/`, `models/mail/`)
- Nome file: `{artifact_name}_v{semver}.joblib` (es. `sms_spam_v1.0.0.joblib`)
- Accanto al binario: `model.json` con metadata

Esempio `model.json`
```json
{
  "name": "sms_spam",
  "version": "1.0.0",
  "created_at": "2025-12-01T12:00:00Z",
  "framework": "scikit-learn",
  "framework_version": "1.7.2",
  "input_example": {"text": "Free entry ..."},
  "output_schema": {"prediction": "spam|ham", "probability_spam": "float"},
  "metrics": {"f1": 0.96, "roc_auc": 0.99},
  "training_commit": "abcdef123",
  "data_hash": "sha256:..."
}
```

Come salvare (snippet)
```python
import joblib
joblib.dump(pipeline, "models/sms/sms_spam_v1.0.0.joblib")
# crea anche models/sms/model.json come sopra
```

Smoke-test rapido (snippet)
```python
import joblib
pipeline = joblib.load("models/sms/sms_spam_v1.0.0.joblib")
print(pipeline.predict(["Hello, how are you?"]))
print(pipeline.predict_proba(["Free money now"]))
```

Best practices
- Registrare versione sklearn/joblib usata.
- Salvare iperparametri e metriche del run.
- Fissare seed per riproducibilità (numpy.random.seed, random.seed).
- Conservare notebook di training e un `validation.ipynb` che mostra esempi di inference su modelli salvati.
- Automatizzare il testing di compatibilità modello ↔ servizio (smoke tests).
