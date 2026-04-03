from flask import Blueprint, jsonify
from app.services.week_days_service import WeekDaysService

# Nome del blueprint al plurale per coerenza con le risorse
week_days_bp = Blueprint("week_days", __name__, url_prefix="/api/week-days")

@week_days_bp.route("", methods=["GET"])
def list_week_days():
    # Recupero dati dal servizio
    items = WeekDaysService.get_all()
    # Trasformazione in lista di dizionari (usa il metodo to_dict del modello)
    return jsonify([item.to_dict() for item in items])

@week_days_bp.route("/<int:week_day_id>", methods=["GET"])
def get_week_day(week_day_id):
    item = WeekDaysService.get_by_id(week_day_id)
    if not item:
        # Standard: 404 se la risorsa non esiste
        return jsonify({"message": "Giorno della settimana non trovato"}), 404
        
    return jsonify(item.to_dict())

# from flask import Blueprint, jsonify
# from app.services.week_days_service import WeekDaysService

# week_days_bp = Blueprint("week_days", __name__, url_prefix="/api/week-days")

# @week_days_bp.route("", methods=["GET"])
# def list_week_days():
#     week_days = WeekDaysService.get_week_days()
#     return jsonify([wd.to_dict() for wd in week_days])

# @week_days_bp.route("/<int:week_day_id>", methods=["GET"])
# def get_week_day(week_day_id):
#     week_day = WeekDaysService.get_week_day_by_id(week_day_id)
#     if not week_day:
#         return jsonify({"error": "Not found"}), 404
#     return jsonify(week_day.to_dict())
