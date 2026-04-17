from app.services.base_service import BaseService
from app.models import db, WorkSchedule, Contract
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

    @classmethod
    def create(cls, data):
        # 1. Pulizia stringhe vuote e conversione tipi base
        processed_data = {}
        for key, value in data.items():
            if value == "":
                processed_data[key] = None
            else:
                processed_data[key] = value

        # 2. Conversione specifica per i campi Time
        time_fields = ['start_time', 'end_time']
        for field in time_fields:
            if processed_data.get(field):
                try:
                    time_str = processed_data[field]
                    processed_data[field] = datetime.strptime(time_str[:5], "%H:%M").time()
                except ValueError:
                    processed_data[field] = None

        # 3. Conversione tipi numerici (se arrivano come stringhe dal form)
        if processed_data.get('weekly_hours'):
            processed_data['weekly_hours'] = float(processed_data['weekly_hours'])
        if processed_data.get('schedule_type_id'):
            processed_data['schedule_type_id'] = int(processed_data['schedule_type_id'])

        # 4. Creazione record
        new_schedule = WorkSchedule(**processed_data)
        db.session.add(new_schedule)
        db.session.commit()
        return new_schedule

    @classmethod
    def update(cls, schedule_id, data):
        schedule = db.session.get(WorkSchedule, schedule_id)
        if not schedule:
            return None
        for key, value in data.items():
            if hasattr(schedule, key):
                setattr(schedule, key, value)
        db.session.commit()
        return cls.get_by_id(schedule_id)