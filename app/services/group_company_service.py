from app.services.base_service import BaseService
from app.models import GroupCompany, Sector, db
from sqlalchemy.orm import joinedload


class GroupCompanyService(BaseService):
    model = GroupCompany
    query_options = [joinedload(GroupCompany.sectors)]

    @classmethod
    def create(cls, data):
        company = GroupCompany(
            name=data.get("name"),
            vat_number=data.get("vat_number")
        )
        sector_ids = data.get("sector_ids", [])
        if sector_ids:
            sectors = Sector.query.filter(Sector.id.in_(sector_ids)).all()
            company.sectors = sectors
        db.session.add(company)
        db.session.commit()
        return company

    @classmethod
    def update(cls, company_id, data):
        company = db.session.get(GroupCompany, company_id)
        if not company:
            return None
        if "name" in data:
            company.name = data["name"]
        if "vat_number" in data:
            company.vat_number = data["vat_number"]
        if "sector_ids" in data:
            sectors = Sector.query.filter(Sector.id.in_(data["sector_ids"])).all()
            company.sectors = sectors
        db.session.commit()
        return company