from .libemax_base import LibemaxBase
from .libemax_mappers import map_richiesta, map_richiesta_tipo


class LibemaxRichiestaService(LibemaxBase):

    def get_list(self, **filters):
        payload = {}
        if filters.get("from"):
            payload["da"] = filters["from"]
        if filters.get("to"):
            payload["a"] = filters["to"]
        if filters.get("inserted_from"):
            payload["data_inserimento_da"] = filters["inserted_from"]
        if filters.get("inserted_to"):
            payload["data_inserimento_a"] = filters["inserted_to"]
        if filters.get("approved") is not None:
            payload["approvata"] = filters["approved"]

        dati = self._post("richiesta/richiesta_elenco", payload)
        items = dati.get("richiesta", [])
        return [map_richiesta(r) for r in items]

    def get_types(self):
        dati = self._post("richiesta/richiesta_tipo_elenco")
        items = dati.get("richiesta_tipo", [])
        return [map_richiesta_tipo(t) for t in items]
