from .libemax_base import LibemaxBase
from .libemax_mappers import map_attivita


class LibemaxAttivitaService(LibemaxBase):

    def get_list(self):
        dati = self._post("attivita/attivita_elenco")
        items = dati.get("attivita", [])
        return [map_attivita(a) for a in items]

    def sync(self, data: dict):
        payload = {}
        if "description" in data:
            payload["descrizione"] = data["description"]
        if "archived" in data:
            payload["archiviato"] = data["archived"]
        if "code" in data:
            payload["codice_gestionale"] = data["code"]

        dati = self._post("attivita/attivita_sincronizza", payload)
        return map_attivita(dati.get("attivita", {}))

    def delete(self, code: str):
        self._post("attivita/attivita_elimina", {"codice_gestionale": code})
        return True
