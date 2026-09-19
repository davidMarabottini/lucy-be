from typing import Any, Dict, List

from app.services.base_service import BaseService
from app.models import db, WorkSchedule, WorkScheduleType, Contract, WeekDay
from sqlalchemy.orm import joinedload
from datetime import datetime

class WorkScheduleService(BaseService):
    model = WorkSchedule
    query_options = [
        joinedload(WorkSchedule.schedule_type),
        joinedload(WorkSchedule.week_day),
        joinedload(WorkSchedule.work_activity),
        # joinedload(WorkSchedule.contract).joinedload(Contract.client)
    ]

    @classmethod
    def get_by_contract(cls, contract_id):
        query = WorkSchedule.query.filter_by(contract_id=contract_id)
        if cls.query_options:
            query = query.options(*cls.query_options)
        return query.all()

    @classmethod
    def create(cls, data):
        processed = cls._process_data(data)
        return super().create(processed)

    @classmethod
    def _apply_updates(cls, entity, data):
        """Override del metodo di BaseService per processare i dati prima di applicarli."""
        processed = cls._process_data(data)
        super()._apply_updates(entity, processed)

    @classmethod
    def _process_data(cls, data):
        """Sanifica i dati in ingresso, convertendo tipi orario, float e int."""
        processed_data = {}
        for key, value in data.items():
            if value == "":
                processed_data[key] = None
            else:
                processed_data[key] = value

        # Conversione campi Time
        time_fields = ['start_time', 'end_time']
        for field in time_fields:
            if processed_data.get(field):
                try:
                    time_str = str(processed_data[field])
                    processed_data[field] = datetime.strptime(time_str[:5], "%H:%M").time()
                except ValueError:
                    processed_data[field] = None

        # Conversione tipi numerici
        if processed_data.get('weekly_hours') is not None:
            try:
                processed_data['weekly_hours'] = float(processed_data['weekly_hours'])
            except (ValueError, TypeError):
                pass

        if processed_data.get('schedule_type_id') is not None:
            try:
                processed_data['schedule_type_id'] = int(processed_data['schedule_type_id'])
            except (ValueError, TypeError):
                pass

        return processed_data


    def sync_contract_schedules(contract_id: int, payload: Dict[str, Any]) -> List[WorkSchedule]:
        DAY_NAME_MAP = {
            "monday": "Lunedì",
            "tuesday": "Martedì",
            "wednesday": "Mercoledì",
            "thursday": "Giovedì",
            "friday": "Venerdì",
            "saturday": "Sabato",
            "sunday": "Domenica"
        }
        # 1. Validazione di coerenza contract_id
        payload_contract_id = payload.get("contract_id")
        if payload_contract_id is not None and int(payload_contract_id) != contract_id:
            raise ValueError(f"Incoerenza contract_id: URL ({contract_id}) != Body ({payload_contract_id})")

        contract = Contract.query.get(contract_id)
        if not contract:
            raise ValueError(f"Contratto con ID {contract_id} non trovato")

        try:
            # 2. Cancelliamo i vecchi orari associati al contratto
            WorkSchedule.query.filter_by(contract_id=contract_id).delete()

            new_schedules = []
            schedule_types = WorkScheduleType.query.all()
            fixed_schedule_types = [schedule_type for schedule_type in schedule_types if schedule_type.period == 'FIXED']
            flexible_schedule_types = {
                schedule_type.name.strip().lower(): schedule_type
                for schedule_type in schedule_types
                if schedule_type.period != 'FIXED'
            }

            # 3. Orari FIXED: ogni fascia viene associata a tutti i tipi FIXED configurati.
            schedules_data = payload.get("schedules", [])
            if not isinstance(schedules_data, list):
                raise ValueError("Il campo 'schedules' deve essere una lista")

            # Cache dei giorni della settimana per velocizzare le query
            week_days_by_name = {wd.name.lower(): wd.id for wd in WeekDay.query.all()}

            for item in schedules_data:
                day_raw = item.get("day", "").lower()
                db_day_name = DAY_NAME_MAP.get(day_raw, day_raw)
                week_day_id = week_days_by_name.get(day_raw) or week_days_by_name.get(db_day_name.lower())

                if not week_day_id:
                    raise ValueError(f"Giorno della settimana non valido: {day_raw}")

                start_time_obj = datetime.strptime(item["startTime"], "%H:%M").time() if item.get("startTime") else None
                end_time_obj = datetime.strptime(item["endTime"], "%H:%M").time() if item.get("endTime") else None

                for schedule_type in fixed_schedule_types:
                    schedule = WorkSchedule(
                        contract_id=contract_id,
                        schedule_type_id=schedule_type.id,
                        week_day_id=week_day_id,
                        start_time=start_time_obj,
                        end_time=end_time_obj,
                        weekly_hours=None
                    )
                    db.session.add(schedule)
                    new_schedules.append(schedule)

            # 4. Orari flessibili: le chiavi dipendono dai nomi dei tipi configurati.
            flexible_data = payload.get("flexible", {})
            if not isinstance(flexible_data, dict):
                raise ValueError("Il campo 'flexible' deve essere un oggetto")

            for type_name, raw_hours in flexible_data.items():
                if raw_hours in (None, ""):
                    continue

                schedule_type = flexible_schedule_types.get(str(type_name).strip().lower())
                if not schedule_type:
                    raise ValueError(f"Tipo di orario flessibile non valido: {type_name}")

                try:
                    weekly_hours = float(raw_hours)
                except (ValueError, TypeError):
                    raise ValueError(f"Il valore di '{type_name}' in flexible deve essere numerico")

                schedule = WorkSchedule(
                    contract_id=contract_id,
                    schedule_type_id=schedule_type.id,
                    week_day_id=None,
                    start_time=None,
                    end_time=None,
                    weekly_hours=weekly_hours
                )
                db.session.add(schedule)
                new_schedules.append(schedule)

            db.session.commit()
            return new_schedules

        except Exception as e:
            db.session.rollback()
            raise e
