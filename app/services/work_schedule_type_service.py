from app.auth.decorators import paginated_response

from ..models import WorkScheduleType, db

class WorkScheduleTypeService:
    @staticmethod
    def get_all():
        """Recupera tutte le tipologie di orario"""
        return WorkScheduleType.query.all()

    @staticmethod
    def get_by_id(wst_id):
        """Recupera una tipologia specifica tramite ID"""
        return db.session.get(WorkScheduleType, wst_id)

    @staticmethod
    def create(data):
        """Crea una nuova tipologia di orario"""
        work_type = WorkScheduleType(
            name=data.get("name"),
            description=data.get("description"),
            frequency=data.get("frequency"),
            period=data.get("period", "NONE"),
            icon_name=data.get("icon_name", "Clock")
        )
        db.session.add(work_type)
        db.session.commit()
        return work_type

    @staticmethod
    def update(wst_id, data):
        """Aggiorna una tipologia esistente"""
        work_type = db.session.get(WorkScheduleType, wst_id)
        if not work_type:
            return None
        
        if "name" in data:
            work_type.name = data["name"]
        if "description" in data:
            work_type.description = data["description"]
        if "frequency" in data:
            work_type.frequency = data["frequency"]
        if "period" in data:
            work_type.period = data["period"]
        if "icon_name" in data:
            work_type.icon_name = data["icon_name"]
            
        db.session.commit()
        return work_type

    @staticmethod
    def delete(wst_id):
        """Elimina una tipologia"""
        work_type = db.session.get(WorkScheduleType, wst_id)
        if not work_type:
            return False
        
        db.session.delete(work_type)
        db.session.commit()
        return True