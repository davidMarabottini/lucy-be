from datetime import datetime
from .libemax_base import LibemaxBase
from .libemax_mappers import map_timbratura


# ── DATI MOCK ─────────────────────────────────────────────────────────────────
# Cliente di riferimento: Condominio Via Settembrini 35, Milano
# Coordinate cliente:      45.4838, 9.1878
# Punto entrata (~200m):   45.4856, 9.1880  (Via Melchiorre Gioia 18)
# Punto uscita  (~3km):    45.5108, 9.2010  (Viale Monza 42)
#
# Struttura raw identica a quella restituita da Libemax (campi in italiano).
# Il mapper map_timbratura() viene applicato nel get_list, come nella chiamata reale.
# ─────────────────────────────────────────────────────────────────────────────

_MOCK_CLIENTE = {
    "id": 3,
    "nome": "Condominio Via Settembrini 35",
    "indirizzo": "Via Settembrini 35",
    "citta": "Milano",
    "cap": "20124",
    "piva": "",
    "email": "amministrazione@condominiosettembrini.it",
    "provincia": "MI",
    "codice_gestionale": "CLI003",
    "latitudine": "45.4838",
    "longitudine": "9.1878",
    "note": "",
    "archiviato": 0,
    "contatto": {
        "id": 3,
        "nome": "Giovanna Ferrario",
        "cellulare": "338 9021456",
        "email": "g.ferrario@condominiosettembrini.it",
    },
}


def _build_mock(da: str) -> dict:
    """
    Simula la risposta raw di Libemax (campo 'dati') per timbratura_elenco.
    Struttura identica a quella restituita dall'API: campi in italiano.
    map_timbratura() viene applicato in get_list, esattamente come nella chiamata reale.

    Restituisce 1 timbratura (turno chiuso):
      - entrata: 200m dal cliente  → Via Melchiorre Gioia 18  (45.4856, 9.1880)
      - uscita:  3km dal cliente   → Viale Monza 42           (45.5108, 9.2010)
    """
    try:
        d = datetime.strptime(da, "%Y-%m-%d")
        date_str = d.strftime("%d/%m/%Y")   # formato Libemax: 15/01/2024
        last_mod = d.strftime("%Y-%m-%d")   # formato ultima_modifica: 2024-01-15
    except ValueError:
        date_str = "01/01/2024"
        last_mod = "2024-01-01"

    return {
        "timbratura": [
            {
                "id": 901,
                "ultima_modifica": f"{last_mod} 16:44:51",
                "ora_inizio":           f"{date_str} 08:02:33",
                "ora_inizio_arrotondata": f"{date_str} 08:00",
                "ora_fine":             f"{date_str} 16:44:51",
                "ore":                  "08:42",
                "ore_arrotondate":      "08:45",
                "pausa":                "01:00",
                "ore_al_netto_della_pausa":           "07:42",
                "ore_arrotondate_al_netto_della_pausa": "07:45",
                "ore_diurno":           "08:42",
                "ore_notturno":         "00:00",
                "ore_diurno_arrotondate":  "08:45",
                "ore_notturno_arrotondate": "00:00",
                # entrata: ~200m dal cliente
                "latitudine_start":  "45.4856",
                "longitudine_start": "9.1880",
                "indirizzo_start":   "Via Melchiorre Gioia 18",
                "cap_start":         "20124",
                "citta_start":       "Milano",
                "provincia_start":   "MI",
                "stato_start":       "Italia",
                # uscita: ~3km dal cliente
                "latitudine_end":    "45.5108",
                "longitudine_end":   "9.2010",
                "indirizzo_end":     "Viale Monza 42",
                "cap_end":           "20127",
                "citta_end":         "Milano",
                "provincia_end":     "MI",
                "stato_end":         "Italia",
                "tag_seriale_start": "",
                "tag_testo_start":   "",
                "seriale_nfc_start": "",
                "tag_seriale_stop":  "",
                "tag_testo_stop":    "",
                "codice_dispositivo": "AND_mock0001aabbcc",
                "note":        "",
                "descrizione": "Turno mattina",
                "cliente": _MOCK_CLIENTE,
                "dipendente": {
                    "id": 1,
                    "nome":               "Marco",
                    "cognome":            "Bianchi",
                    "email":              "m.bianchi@esempio.it",
                    "telefono":           "",
                    "cellulare":          "347 1122334",
                    "codice_gestionale":  "DIP001",
                    "note":               "",
                    "archiviato":         0,
                    "data_cessazione":    None,
                },
                "attivita": None,
                "foglio_intervento": "",
                "allegati":    [],
                "produttivita": [],
                "sblocco_timbratura":  0,
                "timbratura_confermata": 1,
            }
        ]
    }


class LibemaxTimbraturaService(LibemaxBase):

    def get_list(self, da: str, a: str, **filters):
        # ── MOCK ATTIVO ────────────────────────────────────────────────────
        # Dati fittizi per sviluppo frontend — zero chiamate API consumate.
        # Per passare alla chiamata reale: commenta il blocco MOCK e
        # decommenta il blocco CHIAMATA REALE sotto.
        dati = _build_mock(da)
        items = dati.get("timbratura", [])
        # return [map_timbratura(t) for t in items]
        return items
        # ── FINE MOCK ──────────────────────────────────────────────────────

        # ── CHIAMATA REALE ─────────────────────────────────────────────────
        # payload = {"da": da, "a": a}
        # if filters.get("last_modified_from"):
        #     payload["ultima_modifica_da"] = filters["last_modified_from"]
        # if filters.get("last_modified_to"):
        #     payload["ultima_modifica_a"] = filters["last_modified_to"]
        # if filters.get("type"):
        #     payload["tipo"] = filters["type"]
        # if filters.get("employee_code"):
        #     payload["dipendente"] = filters["employee_code"]
        # if filters.get("client_code"):
        #     payload["cliente"] = filters["client_code"]
        # if filters.get("activity_code"):
        #     payload["attivita"] = filters["activity_code"]
        # if filters.get("only_with_code") is not None:
        #     payload["dipendenti_con_codice"] = filters["only_with_code"]
        # if filters.get("format"):
        #     payload["formato"] = filters["format"]
        # dati = self._post("timbratura/timbratura_elenco", payload)
        # items = dati.get("timbratura", [])
        # return [map_timbratura(t) for t in items]
        # ── FINE CHIAMATA REALE ────────────────────────────────────────────

