from .libemax_base import LibemaxBase


class LibemaxOrarioService(LibemaxBase):

    def sync(self, data: dict):
        payload = {}

        # Identificativo dipendente (uno dei due obbligatorio)
        if "employee_code" in data:
            payload["codice_gestionale_dipendente"] = data["employee_code"]
        if "employee_id" in data:
            payload["dipendente_id"] = data["employee_id"]

        # Opzioni
        option_map = {
            "exclude_travel": "orario_lavorativo_trasferta_esclusa",
            "auto_rol": "orario_lavorativo_gestione_automatica_rol",
            "paid_break": "orario_lavorativo_pausa_retribuita",
            "no_auto_break_deduction": "orario_lavorativo_non_scalare_pausa",
            "break_from_overtime": "orario_lavorativo_pausa_scala_da_straordinari",
            "hour_bank": "orario_lavorativo_banca_ore",
            "overtime_approval": "orario_lavorativo_approvazione_straordinari",
        }
        for en_key, it_key in option_map.items():
            if en_key in data:
                payload[it_key] = data[en_key]

        # Ore lavorative per giorno
        days = ["lunedi", "martedi", "mercoledi", "giovedi", "venerdi", "sabato", "domenica"]
        days_en = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        
        hours = data.get("hours", {})
        breaks = data.get("breaks", {})
        for en, it in zip(days_en, days):
            if en in hours:
                payload[f"orario_lavorativo_ore_{it}"] = hours[en]
            if en in breaks:
                payload[f"orario_lavorativo_pausa_{it}"] = breaks[en]

        self._post("orariolavorativo/orariolavorativo_sincronizza", payload)
        return True
