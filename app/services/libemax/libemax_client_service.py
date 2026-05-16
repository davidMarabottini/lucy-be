from .libemax_base import LibemaxBase
from .libemax_mappers import map_cliente


class LibemaxClienteService(LibemaxBase):

    def get_list(self):
        dati = self._post("cliente/cliente_elenco")
        items = dati.get("cliente", [])
        return [map_cliente(c) for c in items]

    def sync(self, data: dict):
        payload = {}
        field_map = {
            "id": "id",
            "code": "codice_gestionale",
            "name": "nome",
            "address": "indirizzo",
            "city": "citta",
            "province": "provincia",
            "country": "stato",
            "zip": "cap",
            "vat": "piva",
            "phone": "telefono",
            "email": "email",
            "latitude": "latitudine",
            "longitude": "longitudine",
            "notes": "note",
            "contact_name": "contatto",
            "contact_mobile": "contatto_cellulare",
            "contact_email": "contatto_email",
            "archived": "archiviato",
        }
        for en_key, it_key in field_map.items():
            if en_key in data:
                payload[it_key] = data[en_key]

        if "employee_ids" in data:
            payload["dipendente_id"] = data["employee_ids"]
        if "employee_codes" in data:
            payload["dipendente_codice_gestionale"] = data["employee_codes"]

        dati = self._post("cliente/cliente_sincronizza", payload)
        return map_cliente(dati.get("cliente", {}))

    def delete(self, identifier: str, by_id: bool = False):
        payload = {"id": identifier} if by_id else {"codice_gestionale": identifier}
        self._post("cliente/cliente_elimina", payload)
        return True