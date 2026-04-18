import os

from flask import Flask
from flask_cors import CORS

from .extension import db, migrate
from .utils.paths import resolve_paths
from .config.logger import configure_logging

from .core import (
    setup_database,
    prepare_temp_db,
    configure_app_db,
    register_cli_commands,
    register_spa_routes,
    create_shutdown_handler,
)

configure_logging()


def create_app(db_password: str, db_path=None):
    base_path, abs_db_path, static_folder = resolve_paths(db_path)

    app = Flask(__name__, static_folder=static_folder)

    # DB temporaneo decriptato
    fernet, tmp_db_path = prepare_temp_db(db_password, abs_db_path)

    # Configurazione SQLAlchemy + sessioni
    configure_app_db(app, tmp_db_path)

    # CORS
    CORS(app, supports_credentials=True, origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5000",
        "http://127.0.0.1:5000",
    ])

    # Init estensioni
    db.init_app(app)
    migrate.init_app(app, db)

    # Import locali e registrazione componenti
    from . import models  # noqa: F401
    from .routes import register_routes
    from .exception import register_error_handlers

    register_routes(app)
    register_error_handlers(app)
    register_cli_commands(app)
    register_spa_routes(app)

    app.setup_database_func = setup_database

    # Shutdown: cifra il DB all'uscita
    create_shutdown_handler(app, fernet, tmp_db_path, abs_db_path)

    return app
