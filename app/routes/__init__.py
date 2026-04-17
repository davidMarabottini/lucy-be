from .auth_routes import auth_bp
from .user_routes import users_bp
from .libemax_routes import libemax_bp
from .clients_routes import clients_bp
from .work_activity_routes import activities_bp
from .work_schedule_route import schedule_bp
from .week_days_routes import week_days_bp
from .sectors_routes import sectors_bp
from .group_company_routes import group_company_bp
from .contract_routes import contracts_bp
from .work_schedule_type_route import wst_bp

def register_routes(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(libemax_bp)
    app.register_blueprint(clients_bp)
    app.register_blueprint(activities_bp)
    app.register_blueprint(schedule_bp)
    app.register_blueprint(sectors_bp)
    app.register_blueprint(group_company_bp)
    app.register_blueprint(contracts_bp)
    app.register_blueprint(wst_bp)
    app.register_blueprint(week_days_bp)
