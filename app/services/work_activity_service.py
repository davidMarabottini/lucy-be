from ..models import WorkActivity, db

class WorkActivityService:
    @staticmethod
    def get_all():
        return WorkActivity.query.all()

    @staticmethod
    def get_by_id(activity_id):
        return db.session.get(WorkActivity, activity_id)

    @staticmethod
    def create(data):
        """Crea una nuova attività (Anagrafica)"""
        activity = WorkActivity(
            name=data.get("name"),           # Nuovo campo
            description=data.get("description")
        )
        db.session.add(activity)
        db.session.commit()
        return activity

    @staticmethod
    def update(activity_id, data):
        """Aggiorna un'attività esistente"""
        activity = db.session.get(WorkActivity, activity_id)
        if not activity:
            return None
        
        # Aggiorna solo i campi presenti nel nuovo modello
        if "name" in data: 
            activity.name = data["name"]
        if "description" in data: 
            activity.description = data["description"]
            
        db.session.commit()
        return activity

    @staticmethod
    def delete(activity_id):
        activity = db.session.get(WorkActivity, activity_id)
        if not activity:
            return False
        db.session.delete(activity)
        db.session.commit()
        return True