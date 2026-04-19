from .libemax_base import LibemaxBase
from .libemax_mappers import map_lavoro_programmato


class LibemaxLavoroProgrammatoService(LibemaxBase):

    def get_list(self, da: str, a: str, **filters):
        payload = {"da": da, "a": a}
        if filters.get("employee_id"):
            payload["dipendente_id"] = filters["employee_id"]

        dati = self._post("lavoro_programmato/lavoro_programmato_elenco", payload)
        items = dati.get("lavoro_programmato", [])
        return [map_lavoro_programmato(lp) for lp in items]

    def sync(self, data: dict):
        payload = {}
        field_map = {
            "date": "data",
            "time": "ora",
            "end_date": "data_fine",
            "end_time": "ora_fine",
            "description": "descrizione",
            "suspended": "sospeso",
            "full_day": "giornata_intera",
            "code": "codice_gestionale",
            "employee_ids": "dipendente_id",
            "client_id": "cliente_id",
            "title": "titolo",
        }
        for en_key, it_key in field_map.items():
            if en_key in data:
                payload[it_key] = data[en_key]

        dati = self._post("lavoro_programmato/lavoro_programmato_sincronizza", payload)
        return map_lavoro_programmato(dati.get("lavoro_programmato", {}))

    def delete(self, code: str):
        self._post("lavoro_programmato/lavoro_programmato_elimina", {"codice_gestionale": code})
        return True
