import os
import logging
import click
import tempfile
import atexit

from flask import Flask, send_from_directory
from flask.cli import with_appcontext
from flask_cors import CORS

from .extension import db, migrate
from .utils.crypto import get_fernet, encrypt_db, decrypt_db
from .utils.paths import resolve_paths
from .config.logger import configure_logging

configure_logging()
_shutdown_executed = False

# -------------------------
# DATABASE SETUP
# -------------------------
def setup_database():
    try:
        db.create_all()
        # Recuperiamo l'URI dalla configurazione dell'app corrente
        from flask import current_app
        db_uri = current_app.config.get("SQLALCHEMY_DATABASE_URI", "Unknown")
        return f"✅ Database creato con successo!\nURI: {db_uri}"
    except Exception as e:
        logging.error(f"Errore durante db.create_all(): {e}")
        return f"❌ Errore durante la creazione delle tabelle: {e}"


def create_app(db_password: str, db_path=None):
    from tkinter import messagebox
    global _shutdown_executed

    base_path, abs_db_path, static_folder = resolve_paths(db_path)

    app = Flask(__name__, static_folder=static_folder)

    _shutdown_executed = False
    # -------------------------
    # FILE TEMPORANEO DB DECRIPTATO
    # -------------------------
    fernet = get_fernet(db_password)
    
    tmp_db_file = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
    tmp_db_path = tmp_db_file.name.replace("\\", "/") # tmp_db_file.name

    tmp_db_file.close()

    if os.path.exists(abs_db_path):
        decrypt_db(db_password, abs_db_path, tmp_db_path)

    else:
        # se non esiste, crea DB vuoto
        open(tmp_db_path, "wb").close()

    # -------------------------
    # CONFIG SQLALCHEMY
    # -------------------------
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{tmp_db_path}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Session config
    app.config.update(
        SESSION_COOKIE_SECURE=False,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
        SESSION_COOKIE_NAME="session",
    )

    # CORS
    CORS(app, supports_credentials=True)

    # Init estensioni
    db.init_app(app)
    migrate.init_app(app, db)

    # -------------------------
    # IMPORT LOCALI
    # -------------------------
    from . import models
    from .models import User, Role, WeekDay
    from .routes import register_routes
    from .exception import register_error_handlers
    from .services.model_registry import ModelRegistry

    register_routes(app)
    register_error_handlers(app)

    app.model_registry = ModelRegistry(root_dir=os.path.join(base_path, "app"))


    app.setup_database_func = setup_database

    # -------------------------
    # STATIC + SPA HANDLER
    # -------------------------
    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def catch_all(path):
        file_path = os.path.join(app.static_folder, path)
        if path and os.path.exists(file_path):
            return send_from_directory(app.static_folder, path)
        if path.startswith("api/"):
            return {"error": "API non trovata"}, 404
        return send_from_directory(app.static_folder, "index.html")

    # -------------------------
    # HELPERS: roles e admin
    # -------------------------
    def ensure_roles():
        admin = Role.query.filter_by(name="admin").first()
        user = Role.query.filter_by(name="user").first()
        if not admin: admin = Role(name="admin")
        if not user: user = Role(name="user")
        db.session.add_all([admin, user])
        db.session.commit()
        return admin, user

    def create_admin_internal(username, email, password):
        admin_role, user_role = ensure_roles()
        if User.query.filter_by(email=email).first():
            return "Errore: Email già esistente."
        user = User(username=username, email=email, name="Admin")
        user.set_password(password)
        user.roles.extend([admin_role, user_role])
        db.session.add(user)
        db.session.commit()
        return f"Admin '{username}' creato."

    @app.cli.command("create-admin")
    @with_appcontext
    def create_admin():
        username = click.prompt("Username")
        email = click.prompt("Email")
        password = click.prompt("Password", hide_input=True, confirmation_prompt=True)
        click.echo(create_admin_internal(username, email, password))

    app.create_admin_func = create_admin_internal

    # -------------------------
    # WEEK DAYS
    # -------------------------
    def create_week_days_internal():
        days = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
        new_days = [WeekDay(name=d) for d in days if not WeekDay.query.filter_by(name=d).first()]
        if new_days:
            db.session.add_all(new_days)
            db.session.commit()
            return f"Creati {len(new_days)} giorni."
        return "Già presenti."

    @app.cli.command("create-week-days")
    @with_appcontext
    def create_week_days():
        click.echo(create_week_days_internal())

    app.create_week_days_func = create_week_days_internal

    # -------------------------
    # CIFRATURA DB ALL'USCITA
    # -------------------------
    def encrypt_db_on_exit():
        
        with open(tmp_db_path, "rb") as f:
            data = f.read()
        encrypted_data = fernet.encrypt(data)
        with open(abs_db_path, "wb") as f:
            f.write(encrypted_data)
        os.remove(tmp_db_path)
        
    # -------------------------
    # SHUTDOWN + CIFRATURA
    # -------------------------
    def shutdown_and_encrypt():
        global _shutdown_executed
        
        if _shutdown_executed or app is None:
            return

        try:
            logging.info("Avvio procedura di chiusura sicura...")
            
            with app.app_context():
                db.session.remove()
                db.engine.dispose()
                
            logging.info("Connessioni DB chiuse.")
            
            import time
            time.sleep(0.5)
            
            if not os.path.exists(tmp_db_path):
                logging.warning("Shutdown: Il file temporaneo non esiste già più.")
                return
            
            if os.path.getsize(tmp_db_path) == 0:
                logging.error("Shutdown: File temporaneo vuoto. Abortisco per evitare perdita dati.")
                return
            
            with open(tmp_db_path, "rb") as f:
                data = f.read()
                
            encrypted_data = fernet.encrypt(data)
            with open(abs_db_path, "wb") as f:
                f.write(encrypted_data)
                
            os.remove(tmp_db_path)
            logging.info("Rimosso file temporaneo.")
            _shutdown_executed = True # Segna come completato
            logging.info("🔒 Database protetto e allineato correttamente.")
            
        except Exception as e:
            logging.error(f"❌ Errore critico durante lo shutdown: {e}")
            raise e

    # Esponi funzione al manager
    app.shutdown_func = shutdown_and_encrypt
    
    atexit.register(shutdown_and_encrypt)

    return app
