from .libemax_base import LibemaxBase
from .libemax_mappers import map_produttivita


class LibemaxProduttivitaService(LibemaxBase):

    def get_list(self):
        dati = self._post("produttivita/produttivita_elenco")
        items = dati.get("produttivita", [])
        return [map_produttivita(p) for p in items]

    def sync(self, data: dict):
        payload = {}
        field_map = {
            "description": "descrizione",
            "value_type": "valore_tipo",
            "client_cost": "costo_cliente",
            "internal_cost": "costo_interno",
            "archived": "archiviato",
            "code": "codice_gestionale",
        }
        for en_key, it_key in field_map.items():
            if en_key in data:
                payload[it_key] = data[en_key]

        dati = self._post("produttivita/produttivita_sincronizza", payload)
        return map_produttivita(dati.get("produttivita", {}))

    def delete(self, code: str):
        self._post("produttivita/produttivita_elimina", {"codice_gestionale": code})
        return True
