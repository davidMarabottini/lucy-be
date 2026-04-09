from app.auth.decorators import paginated_response
from ..models import Sector, db

class SectorService:
    @staticmethod
    @paginated_response
    def get_all():
        """Recupera tutti i settori (es. Pulizie, Portierato, Disinfestazione)"""
        return Sector.query

    @staticmethod
    def get_by_id(sector_id):
        """Recupera un singolo settore tramite ID"""
        return db.session.get(Sector, sector_id)

    @staticmethod
    def create(data):
        """Crea un nuovo settore con nome e descrizione"""
        sector = Sector(
            name=data.get("name"),
            description=data.get("description")
        )
        db.session.add(sector)
        db.session.commit()
        return sector

    @staticmethod
    def update(sector_id, data):
        """Aggiorna i dati di un settore esistente"""
        sector = db.session.get(Sector, sector_id)
        if not sector:
            return None
        
        if "name" in data:
            sector.name = data["name"]
        if "description" in data:
            sector.description = data["description"]
            
        db.session.commit()
        return sector

    @staticmethod
    def delete(sector_id):
        """Elimina un settore"""
        sector = db.session.get(Sector, sector_id)
        if not sector:
            return False
        
        db.session.delete(sector)
        db.session.commit()
        return True