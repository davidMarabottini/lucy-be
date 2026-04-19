from .libemax_base import LibemaxBase
from .libemax_mappers import map_arrotondamento


class LibemaxArrotondamentoService(LibemaxBase):

    def get_list(self):
        dati = self._post("arrotondamento/arrotondamento_elenco")
        # NB: la chiave nella risposta Libemax è "attivita" (bug noto nello swagger)
        items = dati.get("attivita", dati.get("arrotondamento", []))
        return [map_arrotondamento(a) for a in items]
