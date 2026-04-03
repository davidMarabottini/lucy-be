from app.auth.decorators import paginated_response
from sqlalchemy.orm import joinedload

from ..models import GroupCompany, Sector, db

class GroupCompanyService:
    @staticmethod
    @paginated_response
    def get_all():
        """Recupera tutte le società con i loro settori associati"""
        return GroupCompany.query.options(joinedload(GroupCompany.sectors))

    @staticmethod
    def get_by_id(company_id):
        """Recupera una società specifica per ID"""
        return db.session.get(GroupCompany, company_id)

    @staticmethod
    def create(data):
        """
        Crea una nuova società del gruppo.
        Payload atteso: { "name": "...", "vat_number": "...", "sector_ids": [1, 2] }
        """
        company = GroupCompany(
            name=data.get("name"),
            vat_number=data.get("vat_number")
        )
        
        # Gestione Many-to-Many: associamo i settori se presenti
        sector_ids = data.get("sector_ids", [])
        if sector_ids:
            sectors = Sector.query.filter(Sector.id.in_(sector_ids)).all()
            company.sectors = sectors
            
        db.session.add(company)
        db.session.commit()
        return company

    @staticmethod
    def update(company_id, data):
        """Aggiorna i dati della società e sincronizza i settori"""
        company = db.session.get(GroupCompany, company_id)
        if not company:
            return None
        
        if "name" in data:
            company.name = data["name"]
        if "vat_number" in data:
            company.vat_number = data["vat_number"]
            
        # Sincronizzazione dei settori (Molti-a-Molti)
        if "sector_ids" in data:
            sector_ids = data.get("sector_ids", [])
            # Recuperiamo i nuovi oggetti Sector
            sectors = Sector.query.filter(Sector.id.in_(sector_ids)).all()
            # SQLAlchemy sovrascrive automaticamente la vecchia lista nella tabella ponte
            company.sectors = sectors
            
        db.session.commit()
        return company

    @staticmethod
    def delete(company_id):
        """Elimina una società (SQLAlchemy pulirà la tabella ponte grazie alla FK)"""
        company = db.session.get(GroupCompany, company_id)
        if not company:
            return False
        
        db.session.delete(company)
        db.session.commit()
        return True