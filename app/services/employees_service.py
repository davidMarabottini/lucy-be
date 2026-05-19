from app.services.base_service import BaseService
from app.services.libemax.libemax_dipendente_service import LibemaxDipendenteService
from app.extension import db
from app.models import Employee


class EmployeeService(BaseService):
    model = Employee

    @classmethod
    def sync_from_libemax(cls):
        libemax_employees = LibemaxDipendenteService().get_list()

        synced = 0
        for lc in libemax_employees:
            lmx_id = lc.get("id")
            if lmx_id is None:
                continue

            existing = Employee.query.filter_by(libemax_id=lmx_id).first()
            if existing:
                existing.name = lc.get("name") or existing.name
                existing.surname = lc.get("surname") or existing.surname
                existing.email = lc.get("email")
                existing.phone = lc.get("mobile") or lc.get("phone") or existing.phone
            else:
                existing = Employee(
                    libemax_id=lmx_id,
                    name=lc.get("name", ""),
                    surname=lc.get("surname", ""),
                    email=lc.get("email"),
                    phone=lc.get("mobile") or lc.get("phone"),
                )
                db.session.add(existing)
            synced += 1

        db.session.commit()
        return synced
