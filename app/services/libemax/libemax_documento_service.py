from .libemax_base import LibemaxBase
from .libemax_mappers import map_documento


class LibemaxDocumentoService(LibemaxBase):

    def get_list(self, da: str, a: str, **filters):
        payload = {"da": da, "a": a}
        if filters.get("employee_id"):
            payload["dipendente_id"] = filters["employee_id"]

        dati = self._post("documento/documento_elenco", payload)
        items = dati.get("documento", [])
        return [map_documento(d) for d in items]

    def sync(self, data: dict, file_tuple=None):
        payload = {}
        field_map = {
            "title": "titolo",
            "description": "descrizione",
            "date": "data",
            "active": "attivo",
            "read_confirmation": "conferma_lettura",
            "type_id": "tipo_id",
            "types": "tipologie",
            "association": "associazione",
            "employee_id": "dipendente_id",
            "group_id": "gruppo_id",
            "client_id": "cliente_id",
            "alert": "avviso",
            "code": "codice_gestionale",
            "send_notification": "invia_notifica",
            "expiry_date": "data_scadenza",
            "expiring_status_date": "data_stato_in_scadenza",
            "renewed_from_id": "rinnovato_da_id",
            "history_guid": "storico_guid",
        }
        for en_key, it_key in field_map.items():
            if en_key in data:
                payload[it_key] = data[en_key]

        files = {}
        if file_tuple:
            files["documento"] = file_tuple

        dati = self._post_multipart("documento/documento_sincronizza", payload, files)
        return map_documento(dati.get("documento", {}))

    def delete(self, code: str):
        self._post("documento/documento_elimina", {"codice_gestionale": code})
        return True
