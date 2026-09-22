from flask import Blueprint, jsonify
from app.services.week_days_service import WeekDaysService
from app.utils.exporters import resolve_export_format
from ..auth.decorators import requires_auth

# Nome del blueprint al plurale per coerenza con le risorse
week_days_bp = Blueprint("week_days", __name__, url_prefix="/api/week-days")

@week_days_bp.route("", methods=["GET"])
# @requires_auth
def list_week_days():
    items = WeekDaysService.get_all()
    return jsonify(items)

@week_days_bp.route("/export", methods=["GET"])
# @requires_auth
def export_week_days():
    try:
        return WeekDaysService.export(fmt=resolve_export_format())
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@week_days_bp.route("/<int:week_day_id>", methods=["GET"])
# @requires_auth
def get_week_day(week_day_id):
    item = WeekDaysService.get_by_id(week_day_id)
    if not item:
        # Standard: 404 se la risorsa non esiste
        return jsonify({"message": "Giorno della settimana non trovato"}), 404
        
    return jsonify(item.to_dict())
