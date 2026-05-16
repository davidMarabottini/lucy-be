from .libemax_base import LibemaxBase
from .libemax_mappers import map_scansione


class LibemaxScansioneService(LibemaxBase):

    def get_list(self, **filters):
        payload = {}
        if filters.get("from_last_scan"):
            payload["da_data_ultima_scansione"] = filters["from_last_scan"]

        dati = self._post("scansione/scansione_elenco", payload)
        items = dati.get("scansione", [])
        return [map_scansione(s) for s in items]

    def get_detail(self, code: str):
        dati = self._post("scansione/scansione_dettaglio", {"codice_gestionale": code})
        return map_scansione(dati.get("scansione", {}))
