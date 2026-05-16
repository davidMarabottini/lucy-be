from .libemax_base import LibemaxBase
from .libemax_mappers import map_foglio_presenze


class LibemaxFoglioPresenzeService(LibemaxBase):

    def get_list(self, year: str, month: str, rounding: int, format_type: int, **filters):
        payload = {
            "anno": year,
            "mese": month,
            "arrotondamento": rounding,
            "formato": format_type,
        }
        if filters.get("only_with_code") is not None:
            payload["dipendenti_con_codice"] = filters["only_with_code"]
        if filters.get("employee_code"):
            payload["dipendente"] = filters["employee_code"]

        dati = self._post("fogliopresenze/fogliopresenze_elenco", payload)
        items = dati.get("fogliopresenze", [])
        return [map_foglio_presenze(fp) for fp in items]
