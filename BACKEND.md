# Backend (Flask) — Notes operative

Scopo
- API WSGI per inferenza dei modelli (sms, mail).
- Minimal, production-aware: health, logging, error handler, model registry (lazy-load).

Requisiti
- Python 3.10+ (consigliato)
- dipendenze: `pip install -r requirements.txt`

Variabili d'ambiente utili
- FLASK_RUN_HOST (default 127.0.0.1)
- FLASK_RUN_PORT (default 5000)
- FLASK_DEBUG (0|1)
- LOG_LEVEL (INFO|DEBUG|WARNING|ERROR)

Avvio
- Sviluppo: `python run.py`
- Produzione: `gunicorn -w 4 "run:app" --bind 0.0.0.0:8000`

Endpoints principali
- GET /predict/<model_type>?text=...  
  - model_type: `sms` o `mail`
  - restituisce JSON: {status, model_used, input_text, prediction, probability_spam}
- GET /health  
  - Restituisce 200 con `{ "status": "ok" }`

Error handling e logging
- Errori controllati -> APIError con status_code restituito in JSON.
- Errori non gestiti -> 500 con messaggio generico; stack logged su stderr.
- LOG_LEVEL controlla livello globale.

Model registry
- I modelli risiedono in `models/`. Il ModelRegistry esegue lazy-load, thread-safe.
- Nomi attesi: `sms_spam_pipeline.joblib`, `mail_spam_pipeline.joblib` (meglio: aggiungere versione).
- Non fare `joblib.load` su payload non trusted.

Sicurezza e robustezza
- Validare `text` (length limit, tipo stringa) prima dell'inferenza.
- Considerare rate limiting, CORS e headers security in produzione.
- Non esportare segreti nel repo; usare .env o secret manager.

Testing e smoke tests
- Implementare uno script di smoke test che carica il modello salvato e esegue inferenze su esempi noti.
- Integrare smoke test in CI per verificare compatibilità modello ↔ servizio.
