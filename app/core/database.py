import os
import logging
import tempfile

from ..extension import db
from ..utils.crypto import get_fernet, decrypt_db


def setup_database():
    try:
        db.create_all()
        from flask import current_app
        db_uri = current_app.config.get("SQLALCHEMY_DATABASE_URI", "Unknown")
        return f"✅ Database creato con successo!\nURI: {db_uri}"
    except Exception as e:
        logging.error(f"Errore durante db.create_all(): {e}")
        return f"❌ Errore durante la creazione delle tabelle: {e}"


def prepare_temp_db(db_password, abs_db_path):
    """Decripta il DB in un file temporaneo e restituisce (fernet, tmp_db_path)."""
    fernet = get_fernet(db_password)

    tmp_db_file = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
    tmp_db_path = tmp_db_file.name.replace("\\", "/")
    tmp_db_file.close()

    if os.path.exists(abs_db_path):
        decrypt_db(db_password, abs_db_path, tmp_db_path)
    else:
        open(tmp_db_path, "wb").close()

    return fernet, tmp_db_path


def configure_app_db(app, tmp_db_path):
    """Configura SQLAlchemy e le sessioni sull'app Flask."""
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{tmp_db_path}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.config.update(
        SESSION_COOKIE_SECURE=False,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
        SESSION_COOKIE_NAME="session",
    )
