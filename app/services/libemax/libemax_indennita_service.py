from .libemax_base import LibemaxBase
from .libemax_mappers import map_indennita, map_indennita_tipo


class LibemaxIndennitaService(LibemaxBase):

    def get_list(self, da: str, a: str, **filters):
        payload = {"da": da, "a": a}
        if filters.get("status") is not None:
            payload["stato"] = filters["status"]
        if filters.get("reimbursed") is not None:
            payload["rimborsata"] = filters["reimbursed"]

        dati = self._post("indennita/indennita_elenco", payload)
        items = dati.get("indennita", [])
        return [map_indennita(i) for i in items]

    def get_types(self):
        dati = self._post("indennita/indennita_tipo_elenco")
        items = dati.get("indennita_tipo", [])
        return [map_indennita_tipo(t) for t in items]
