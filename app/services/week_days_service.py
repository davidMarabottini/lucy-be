from ..models import WeekDay, db

class WeekDaysService:
    @staticmethod
    def get_all():
        """Ritorna tutti i giorni della settimana ordinati"""
        return WeekDay.query.order_by(WeekDay.id.asc()).all()
    
    @staticmethod
    def get_by_id(week_day_id):
        """Ritorna un giorno specifico"""
        # Usiamo get direttamente poiché è una lookup semplice su PK
        return db.session.get(WeekDay, week_day_id)
    
