"""Funzioni di mapping Libemax (IT) → Frontend (EN) condivise tra tutti i service."""


def map_dipendente(d):
    if not d:
        return None
    return {
        "id": d.get("id"),
        "name": d.get("nome"),
        "surname": d.get("cognome"),
        "email": d.get("email"),
        "phone": d.get("telefono"),
        "mobile": d.get("cellulare"),
        "code": d.get("codice_gestionale"),
        "notes": d.get("note"),
        "archived": d.get("archiviato"),
        "termination_date": d.get("data_cessazione"),
        "internal_hourly_cost": d.get("costo_orario_interno"),
        "client_hourly_cost": d.get("costo_orario_cliente"),
    }


def map_cliente(c):
    if not c:
        return None
    contatto = c.get("contatto")
    return {
        "id": c.get("id"),
        "name": c.get("nome"),
        "address": c.get("indirizzo"),
        "city": c.get("citta"),
        "zip": c.get("cap"),
        "vat": c.get("piva"),
        "email": c.get("email"),
        "province": c.get("provincia"),
        "country": c.get("stato"),
        "code": c.get("codice_gestionale"),
        "latitude": c.get("latitudine"),
        "longitude": c.get("longitudine"),
        "notes": c.get("note"),
        "archived": c.get("archiviato"),
        "client_cost_variation": c.get("variazione_costo_cliente"),
        "contact": {
            "id": contatto.get("id"),
            "name": contatto.get("nome"),
            "mobile": contatto.get("cellulare"),
            "email": contatto.get("email"),
        } if contatto else None,
    }


def map_attivita(a):
    if not a:
        return None
    return {
        "id": a.get("id"),
        "description": a.get("descrizione"),
        "code": a.get("codice_gestionale"),
        "archived": a.get("archiviato"),
    }


def map_produttivita(p):
    if not p:
        return None
    return {
        "id": p.get("id"),
        "description": p.get("descrizione"),
        "code": p.get("codice_gestionale"),
        "value_type": p.get("valore_tipo"),
        "client_cost": p.get("costo_cliente"),
        "internal_cost": p.get("costo_interno"),
        "archived": p.get("archiviato"),
    }


def map_produttivita_timbratura(p):
    if not p:
        return None
    return {
        "id": p.get("id"),
        "description": p.get("descrizione"),
        "code": p.get("codice_gestionale"),
        "value_type": p.get("valore_tipo"),
        "client_cost": p.get("costo_cliente"),
        "internal_cost": p.get("costo_interno"),
        "value": p.get("valore"),
    }


def map_allegato(a):
    if not a:
        return None
    return {
        "id": a.get("id"),
        "type": a.get("tipo"),
        "file_url": a.get("file"),
    }


def map_timbratura(t):
    if not t:
        return None
    return {
        "id": t.get("id"),
        "last_modified": t.get("ultima_modifica"),
        "start_time": t.get("ora_inizio"),
        "start_time_rounded": t.get("ora_inizio_arrotondata"),
        "end_time": t.get("ora_fine"),
        "hours": t.get("ore"),
        "hours_rounded": t.get("ore_arrotondate"),
        "pause": t.get("pausa"),
        "net_hours": t.get("ore_al_netto_della_pausa"),
        "net_hours_rounded": t.get("ore_arrotondate_al_netto_della_pausa"),
        "day_hours": t.get("ore_diurno"),
        "night_hours": t.get("ore_notturno"),
        "day_hours_rounded": t.get("ore_diurno_arrotondate"),
        "night_hours_rounded": t.get("ore_notturno_arrotondate"),
        "start_location": {
            "latitude": t.get("latitudine_start"),
            "longitude": t.get("longitudine_start"),
            "address": t.get("indirizzo_start"),
            "zip": t.get("cap_start"),
            "city": t.get("citta_start"),
            "province": t.get("provincia_start"),
            "country": t.get("stato_start"),
        },
        "end_location": {
            "latitude": t.get("latitudine_end"),
            "longitude": t.get("longitudine_end"),
            "address": t.get("indirizzo_end"),
            "zip": t.get("cap_end"),
            "city": t.get("citta_end"),
            "province": t.get("provincia_end"),
            "country": t.get("stato_end"),
        },
        "tag_serial_start": t.get("tag_seriale_start"),
        "tag_text_start": t.get("tag_testo_start"),
        "nfc_serial_start": t.get("seriale_nfc_start"),
        "tag_serial_stop": t.get("tag_seriale_stop"),
        "tag_text_stop": t.get("tag_testo_stop"),
        "device_code": t.get("codice_dispositivo"),
        "notes": t.get("note"),
        "description": t.get("descrizione"),
        "intervention_sheet_url": t.get("foglio_intervento"),
        "attachments": [map_allegato(a) for a in (t.get("allegati") or [])],
        "productivity": [map_produttivita_timbratura(p) for p in (t.get("produttivita") or [])],
        "client": map_cliente(t.get("cliente")),
        "employee": map_dipendente(t.get("dipendente")),
        "activity": map_attivita(t.get("attivita")),
        "unlock_clockin": t.get("sblocco_timbratura"),
        "confirmed": t.get("timbratura_confermata"),
    }


def map_arrotondamento(a):
    if not a:
        return None
    return {
        "id": a.get("id"),
        "timesheet_minute_limit": a.get("fogliopresenze_minuti_limite"),
        "timesheet_slot": a.get("fogliopresenze_slot"),
        "start_minute_limit": a.get("inizio_minuti_limite"),
        "start_slot": a.get("inizio_slot"),
        "end_minute_limit": a.get("fine_minuti_limite"),
        "end_slot": a.get("fine_slot"),
        "timesheet_as_clockin": a.get("fogliopresenze_come_timbratura"),
        "name": a.get("nome"),
        "created_at": a.get("data_creazione"),
    }


def map_richiesta(r):
    if not r:
        return None
    tipo = r.get("tipo")
    return {
        "id": r.get("id"),
        "inserted_at": r.get("data_inserimento"),
        "start_date": r.get("data_inizio"),
        "end_date": r.get("data_fine"),
        "full_day": r.get("giornata_intera"),
        "approval_date": r.get("data_approvazione"),
        "rejection_date": r.get("data_rifiuto"),
        "cancellation_requested_date": r.get("data_annullamento_richiesto"),
        "cancellation_rejected_date": r.get("data_annullamento_rifiutato"),
        "cancellation_approved_date": r.get("data_annullamento_approvato"),
        "status": r.get("stato"),
        "notes": r.get("note"),
        "cancellation_notes": r.get("note_annullamento"),
        "rejection_notes": r.get("note_rifiuto"),
        "cancellation_rejection_notes": r.get("note_annullamento_rifiutato"),
        "employee": map_dipendente(r.get("dipendente")),
        "type": {
            "id": tipo.get("id"),
            "description": tipo.get("descrizione"),
            "code": tipo.get("codice_gestionale"),
        } if tipo else None,
    }


def map_richiesta_tipo(t):
    if not t:
        return None
    return {
        "id": t.get("id"),
        "description": t.get("descrizione"),
    }


def map_nota_spesa(n):
    if not n:
        return None
    tipo = n.get("tipo")
    pagamento = n.get("pagamento")
    return {
        "id": n.get("id"),
        "inserted_at": n.get("data_inserimento"),
        "date": n.get("data"),
        "approval_date": n.get("data_approvazione"),
        "reimbursement_date": n.get("data_rimborso"),
        "amount": n.get("importo"),
        "attachment_url": n.get("allegato_url"),
        "currency_code": n.get("isocode"),
        "exchange_rate": n.get("avgrate"),
        "notes": n.get("note"),
        "mileage_cost": n.get("costo_chilometrico"),
        "km": n.get("km"),
        "client": map_cliente(n.get("cliente")),
        "employee": map_dipendente(n.get("dipendente")),
        "type": {"id": tipo.get("id"), "description": tipo.get("descrizione")} if tipo else None,
        "payment": {"id": pagamento.get("id"), "description": pagamento.get("descrizione")} if pagamento else None,
    }


def map_indennita(i):
    if not i:
        return None
    tipo = i.get("tipo")
    return {
        "id": i.get("id"),
        "inserted_at": i.get("data_inserimento"),
        "date": i.get("data"),
        "notes": i.get("note"),
        "approval_date": i.get("data_approvazione"),
        "rejection_notes": i.get("note_rifiuto"),
        "rejection_date": i.get("data_rifiuto"),
        "reimbursed": i.get("rimborsata"),
        "status": i.get("stato"),
        "amount": i.get("importo"),
        "employee": map_dipendente(i.get("dipendente")),
        "type": {"id": tipo.get("id"), "description": tipo.get("descrizione")} if tipo else None,
    }


def map_indennita_tipo(t):
    if not t:
        return None
    return {
        "id": t.get("id"),
        "description": t.get("descrizione"),
    }


def map_foglio_presenze_entry(entry):
    if not entry:
        return None
    return {
        "date": entry.get("data"),
        "expected_hours": entry.get("ore_previste"),
        "regular_day": entry.get("ordinario_diurno"),
        "regular_night": entry.get("ordinario_notturno"),
        "travel_day": entry.get("ore_viaggio_diurno"),
        "travel_night": entry.get("ore_viaggio_notturno"),
        "overtime_day": entry.get("straordinario_diurno"),
        "overtime_night": entry.get("straordinario_notturno"),
        "justifications": [
            {"hours": g.get("ore"), "type": g.get("tipo")}
            for g in (entry.get("giustifiche") or [])
        ],
        "total": entry.get("totale"),
    }


def map_foglio_presenze(fp):
    if not fp:
        return None
    return {
        "employee": map_dipendente(fp.get("dipendente")),
        "timesheet": [map_foglio_presenze_entry(e) for e in (fp.get("fogliopresenze") or [])],
    }


def map_scansione(s):
    if not s:
        return None
    return {
        "privacy_date": s.get("privacy_data"),
        "date": s.get("data"),
        "last_check_date": s.get("ultima_verifica_data"),
        "last_valid_check_date": s.get("ultima_verifica_valida_data"),
        "last_check_result": s.get("ultima_verifica_esito"),
        "require_greenpass": s.get("obbliga_greenpass"),
        "today_result": s.get("esito_odierno"),
        "check": s.get("controllo"),
        "type": s.get("tipo"),
        "employee": map_dipendente(s.get("dipendente")),
    }


def map_documento(d):
    if not d:
        return None
    tipo = d.get("tipo")
    return {
        "id": d.get("id"),
        "title": d.get("titolo"),
        "description": d.get("descrizione"),
        "active": d.get("attivo"),
        "alert": d.get("avviso"),
        "filename": d.get("nome_file"),
        "date": d.get("data"),
        "version_date": d.get("versione_data"),
        "code": d.get("codice_gestionale"),
        "read_confirmation": d.get("conferma_lettura"),
        "type": {"id": tipo.get("id"), "name": tipo.get("nome")} if tipo else None,
        "association": d.get("associazione"),
        "client_id": d.get("cliente_id"),
        "employee_id": d.get("dipendente_id"),
        "group_id": d.get("gruppo_id"),
        "expiry_date": d.get("data_scadenza"),
        "expiring_status_date": d.get("data_stato_in_scadenza"),
        "renewed_from_id": d.get("rinnovato_da_id"),
        "history_guid": d.get("storico_guid"),
    }


def map_lavoro_programmato(lp):
    if not lp:
        return None
    return {
        "id": lp.get("id"),
        "date": lp.get("data"),
        "time": lp.get("ora"),
        "end_date": lp.get("data_fine"),
        "end_time": lp.get("ora_fine"),
        "description": lp.get("descrizione"),
        "suspended": lp.get("sospeso"),
        "full_day": lp.get("giornata_intera"),
        "code": lp.get("codice_gestionale"),
        "employee_ids": lp.get("dipendente_id"),
        "client_id": lp.get("cliente_id"),
        "title": lp.get("titolo"),
    }


def map_accesso(a):
    if not a:
        return None
    return {
        "id": a.get("id"),
        "name": a.get("nome"),
        "surname": a.get("cognome"),
        "email": a.get("email"),
        "phone": a.get("telefono"),
        "mobile": a.get("cellulare"),
        "code": a.get("codice_gestionale"),
        "notes": a.get("note"),
        "view_mode": a.get("visualizzazione"),
        "all_clients": a.get("associa_tutti_clienti"),
        "export_scheduled_work": a.get("esporta_lavoro_programmato"),
    }
