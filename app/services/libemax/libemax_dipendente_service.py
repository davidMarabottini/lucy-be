from .libemax_base import LibemaxBase
from .libemax_mappers import map_dipendente


class LibemaxDipendenteService(LibemaxBase):

    def get_list(self):
        dati = self._post("dipendente/dipendente_elenco")
        items = dati.get("dipendente", [])
        return [map_dipendente(d) for d in items]

    def sync(self, data: dict):
        payload = {}
        field_map = {
            "code": "codice_gestionale",
            "surname": "cognome",
            "name": "nome",
            "phone": "telefono",
            "mobile": "cellulare",
            "group_id": "gruppo_id",
            "badge": "badge",
            "termination_date": "data_cessazione",
            "notes": "note",
            "fiscal_code": "codicefiscale",
            "email": "email",
            "username": "username",
            "password": "password",
            "archived": "archiviato",
            "rounding_id": "arrotondamento_id",
            "auto_credentials": "credenziali_automatiche",
            "send_email": "invia_email",
            "internal_hourly_cost": "permesso_speciale_costo_orario_interno",
            "client_hourly_cost": "permesso_speciale_costo_orario_cliente",
            "mileage_cost": "dipendente_costo_chilometrico",
            "web_clock_ip": "permesso_speciale_timbra_web_ip",
        }
        for en_key, it_key in field_map.items():
            if en_key in data:
                payload[it_key] = data[en_key]

        # ID per update
        if "id" in data:
            payload["id"] = data["id"]

        # Permessi speciali (passati come dict "permissions")
        permissions_map = {
            "tag_only": "permesso_speciale_timbra_solo_con_tag",
            "notes_in_clockin": "permesso_speciale_note_in_timbratura",
            "hide_intervention_sheet": "permesso_speciale_no_foglio_intervento",
            "clock_only": "permesso_speciale_solo_timbrare",
            "force_gps": "permesso_speciale_obbliga_gps_attivo",
            "web_realtime_only": "permesso_speciale_timbra_web_temporeale",
            "forgot_start": "permesso_speciale_attiva_dimenticato_start",
            "force_activity": "permesso_speciale_obbliga_attivita",
            "force_productivity": "permesso_speciale_obbliga_produttivita",
            "force_greenpass": "permesso_speciale_obbliga_greenpass",
            "plate_only": "permesso_speciale_timbra_solo_con_targa",
            "push_notifications": "permesso_speciale_invia_notifiche",
            "geofence_start": "permesso_speciale_geofence",
            "geofence_stop": "permesso_speciale_geofence_stop",
            "no_description_prompt": "permesso_speciale_open_descrizione_no",
            "manual_pause": "permesso_speciale_pausa_manuale",
            "forgot_stop": "permesso_speciale_attiva_dimenticato_stop",
            "intervention_sheet_email": "permesso_speciale_attiva_mail_foglio_intervento",
            "manual_allowance": "permesso_speciale_indennita_manuale",
            "tag_management": "permesso_speciale_gestione_tag",
            "add_client_from_app": "permesso_speciale_inserisci_nuovo_cliente",
            "edit_clockin_from_app": "permesso_speciale_modifica_timbratura_da_app",
            "single_intervention_sheet": "permesso_speciale_foglio_intervento_unico",
            "who_in_office": "permesso_speciale_chi_in_ufficio",
            "app_timecard": "permesso_speciale_attiva_cartellino_app",
            "app_timecard_hours": "permesso_speciale_attiva_cartellino_app_orari",
            "app_timecard_employee_hours": "permesso_speciale_attiva_cartellino_app_orari_dipendente",
            "company_holiday_plan": "permesso_speciale_piano_ferie_aziendale",
            "bulk_clockin": "permesso_speciale_timbrature_inserimento_massivo",
            "exclude_attendance_chart": "dipendente_escludi_in_grafico_presenze",
            "disable_attendance_app_login": "permesso_speciale_disattiva_login_app_rilevazione_presenze",
            "disable_mobile_clock_login": "permesso_speciale_disattiva_login_app_timbratirce_mobile",
            "permission_request_email": "permesso_speciale_email_richiesta_permessi",
            "document_expiry_email": "permesso_speciale_email_scadenza_documenti",
            "frozen_user": "permesso_speciale_utente_congelato",
            "credit_alert_email": "dipendente_email_avviso_credito",
            "old_clockin_deletion_days": "permesso_speciale_cancellazione_timbrature_vecchie",
        }
        perms = data.get("permissions", {})
        for en_key, it_key in permissions_map.items():
            if en_key in perms:
                payload[it_key] = perms[en_key]

        # Associazioni clienti
        if "client_ids" in data:
            payload["cliente_id"] = data["client_ids"]
        if "client_codes" in data:
            payload["cliente_codice_gestionale"] = data["client_codes"]

        dati = self._post("dipendente/dipendente_sincronizza", payload)
        return map_dipendente(dati.get("dipendente", {}))

    def delete(self, identifier: str, by_id: bool = False):
        payload = {"id": identifier} if by_id else {"codice_gestionale": identifier}
        self._post("dipendente/dipendente_elimina", payload)
        return True
