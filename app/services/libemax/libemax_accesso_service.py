from .libemax_base import LibemaxBase
from .libemax_mappers import map_accesso


class LibemaxAccessoService(LibemaxBase):

    def get_list(self):
        dati = self._post("accesso/accesso_elenco")
        # NB: la chiave nella risposta Libemax potrebbe essere "lavoro_programmato" (bug noto nello swagger)
        items = dati.get("accesso", dati.get("lavoro_programmato", []))
        if isinstance(items, dict):
            items = [items]
        return [map_accesso(a) for a in items]

    def sync(self, data: dict):
        payload = {}
        field_map = {
            "id": "id",
            "surname": "cognome",
            "name": "nome",
            "username": "username",
            "password": "password",
            "email": "email",
            "phone": "telefono",
            "mobile": "cellulare",
            "code": "codice_gestionale",
            "notes": "note",
            "send_email": "invia_email",
            "view_mode": "visualizzazione",
            "export_scheduled_work": "esporta_lavoro_programmato",
            "all_clients": "associa_tutti_clienti",
            "auto_credentials": "credenziali_automatiche",
            "description": "descrizione",
        }
        for en_key, it_key in field_map.items():
            if en_key in data:
                payload[it_key] = data[en_key]

        if "client_ids" in data:
            payload["cliente_id"] = data["client_ids"]

        self._post("accesso/accesso_sincronizza", payload)
        return True

    def delete(self, identifier: str, by_id: bool = False):
        payload = {"id": identifier} if by_id else {"codice_gestionale": identifier}
        self._post("accesso/accesso_elimina", payload)
        return True
