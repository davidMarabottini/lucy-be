import os
import sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import click
from flask.cli import with_appcontext
import logging
from flask_cors import CORS


db = SQLAlchemy()
migrate = Migrate()

def configure_logging():
    level = os.getenv("LOG_LEVEL", "INFO").upper()
    logging.basicConfig(
        level=getattr(logging, level, logging.INFO),
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )


def create_app():
    app = Flask(__name__)
    
    CORS(app, resources={
        r"/*": {
            "origins": ["http://localhost:5173", "http://localhost:4173"],
            "methods": ["GET", "PUT", "DELETE", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type", "X-Origin-Site"],
            "supports_credentials": True
        }
    })

    
    app_root = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(app_root)
    db_path = os.path.join(project_root, 'spam_analyzer.db')
    
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)

    from . import models

    from .routes import register_routes
    from .exception import register_error_handlers
    from .services.model_registry import ModelRegistry

    register_error_handlers(app)
    register_routes(app)
    
    app.model_registry = ModelRegistry(root_dir=app_root)
    
    @app.cli.command("create-admin")
    @with_appcontext
    def create_admin():
        """Crea un utente admin con ruoli multipli."""
        from .models import User, Role, db
        import click
        
        admin_role = Role.query.filter_by(name='admin').first()
        user_role = Role.query.filter_by(name='user').first()
        
        if not admin_role or not user_role:
            if not admin_role: admin_role = Role(name='admin')
            if not user_role: user_role = Role(name='user')
            db.session.add_all([admin_role, user_role])
            db.session.commit()

        username = click.prompt("Username")
        email = click.prompt("Email")
        password = click.prompt("Password", hide_input=True, confirmation_prompt=True)

        if User.query.filter_by(email=email).first():
            click.echo("Errore: Email già esistente.")
            return

        new_admin = User(username=username, email=email, name="Admin")
        new_admin.set_password(password)
        
        new_admin.roles.append(admin_role)
        new_admin.roles.append(user_role)
        
        db.session.add(new_admin)
        db.session.commit()
        click.echo(f"Utente Admin '{username}' creato con successo con ruoli: admin, user")

    @app.cli.command("create-week-days")
    @with_appcontext
    def create_week_days():
        from .models import WeekDay, db
        import click

        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        
        new_days = []
        for day in days:
            if not WeekDay.query.filter_by(name=day).first():
                new_days.append(WeekDay(name=day))
        
        if new_days:
            db.session.add_all(new_days)
            db.session.commit()
            click.echo(f"Creati {len(new_days)} nuovi giorni.")
        else:
            click.echo("I giorni della settimana sono già presenti.")
            
    return app
