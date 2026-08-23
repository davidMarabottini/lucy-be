from app.services.base_service import BaseService
from app.models import db, WorkSchedule, Contract, WeekDay
from sqlalchemy.orm import joinedload
from datetime import datetime

class WorkScheduleService(BaseService):
    model = WorkSchedule
    query_options = [
        joinedload(WorkSchedule.schedule_type),
        joinedload(WorkSchedule.week_day),
        joinedload(WorkSchedule.work_activity),
        joinedload(WorkSchedule.contract).joinedload(Contract.client)
    ]

    DAYS_MAP = {
        'monday': 'Monday',
        'tuesday': 'Tuesday',
        'wednesday': 'Wednesday',
        'thursday': 'Thursday',
        'friday': 'Friday',
        'saturday': 'Saturday',
        'sunday': 'Sunday'
    }
    
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

    @classmethod
    def sync_contract_schedules(cls, contract_id, payload):
        schedule_type_id = payload.get('schedule_type_id')
        note = payload.get('note')
        weekly_hours = payload.get('weekly_hours')
        schedules = payload.get('schedules', [])

        if not contract_id or not schedule_type_id:
            raise ValueError("contract_id e schedule_type_id sono obbligatori")

        week_days_db = {wd.name.lower(): wd.id for wd in WeekDay.query.all()}

        try:
            # Rimuove i vecchi orari associati al contratto
            WorkSchedule.query.filter_by(contract_id=contract_id).delete()

            # Crea i nuovi record
            for item in schedules:
                day_name = str(item.get('day', '')).lower()
                week_day_id = week_days_db.get(day_name)
                start_str = item.get('startTime')
                end_str = item.get('endTime')

                if not week_day_id or not start_str or not end_str:
                    continue

                start_time = datetime.strptime(start_str[:5], "%H:%M").time()
                end_time = datetime.strptime(end_str[:5], "%H:%M").time()

                new_schedule = WorkSchedule(
                    contract_id=contract_id,
                    schedule_type_id=schedule_type_id,
                    week_day_id=week_day_id,
                    start_time=start_time,
                    end_time=end_time,
                    note=note,
                    weekly_hours=weekly_hours
                )
                db.session.add(new_schedule)

            db.session.commit()
            return WorkSchedule.query.filter_by(contract_id=contract_id).all()

        except Exception as e:
            db.session.rollback()
            raise e