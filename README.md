# Bayes spam detector — BE

Small descrption
- Flask API for SMS and email spam classification.
- Models saved in `models/`; logic in `app/`.

## Quickstart (dev)
### 1. Crea virtual environmente:
```
python -m venv venv
.\venv\Scripts\activate # windows
source venv/bin/activate # linux and mac
```

### 2. Dependences install
```
pip install -r requirements.txt
```

### 3. Virtual enviroment
Creare il file .env nella root di progetto con le seguenti variabili
```
FLASK_APP=run.py
FLASK_ENV=development
FLASK_DEBUG=1
DATABASE_URL=sqlite:///app.db
```

### 4. Database and eventually admin creation admin
```
python -m flask db upgrade
python -m flask create-admin # se si vuole creare utente admin
```

### 5. startup
```
python -m flask run
```

Documents
- BACKEND.md — Backend details.
- MODELS.md — Conventions for artifact models and metadata.
