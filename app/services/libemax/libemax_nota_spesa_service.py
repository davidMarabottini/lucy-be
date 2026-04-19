from .libemax_base import LibemaxBase
from .libemax_mappers import map_nota_spesa


class LibemaxNotaSpesaService(LibemaxBase):

    def get_list(self, da: str, a: str, **filters):
        payload = {"da": da, "a": a}
        if filters.get("approved") is not None:
            payload["approvata"] = filters["approved"]

        dati = self._post("notaspesa/notaspesa_elenco", payload)
        items = dati.get("notaspesa", [])
        return [map_nota_spesa(n) for n in items]
