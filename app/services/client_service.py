from app.services.base_service import BaseService
from app.services.libemax.libemax_client_service import LibemaxClienteService
from app.extension import db
from app.models import Client


class ClientService(BaseService):
    model = Client

    @classmethod
    def sync_from_libemax(cls):
        libemax_clients = LibemaxClienteService().get_list()

        synced = 0
        for lc in libemax_clients:
            lmx_id = lc.get("id")
            if lmx_id is None:
                continue

            existing = Client.query.filter_by(libemax_id=lmx_id).first()
            if existing:
                existing.name = lc.get("name") or existing.name
                existing.email = lc.get("email")
                existing.phone = lc.get("contact", {}).get("mobile") if lc.get("contact") else existing.phone
            else:
                existing = Client(
                    libemax_id=lmx_id,
                    name=lc.get("name", ""),
                    email=lc.get("email"),
                    phone=lc.get("contact", {}).get("mobile") if lc.get("contact") else None,
                )
                db.session.add(existing)
            synced += 1

        db.session.commit()
        return synced
