from .libemax_base import LibemaxBase
from .libemax_mappers import map_timbratura


class LibemaxTimbraturaService(LibemaxBase):

    def get_list(self, da: str, a: str, **filters):
        payload = {"da": da, "a": a}
        if filters.get("last_modified_from"):
            payload["ultima_modifica_da"] = filters["last_modified_from"]
        if filters.get("last_modified_to"):
            payload["ultima_modifica_a"] = filters["last_modified_to"]
        if filters.get("type"):
            payload["tipo"] = filters["type"]
        if filters.get("employee_code"):
            payload["dipendente"] = filters["employee_code"]
        if filters.get("client_code"):
            payload["cliente"] = filters["client_code"]
        if filters.get("activity_code"):
            payload["attivita"] = filters["activity_code"]
        if filters.get("only_with_code") is not None:
            payload["dipendenti_con_codice"] = filters["only_with_code"]
        if filters.get("format"):
            payload["formato"] = filters["format"]

        dati = self._post("timbratura/timbratura_elenco", payload)
        items = dati.get("timbratura", [])
        return [map_timbratura(t) for t in items]
