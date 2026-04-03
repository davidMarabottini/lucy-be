from ..models import db, WorkSchedule, Contract
from sqlalchemy.orm import joinedload
from datetime import datetime

class WorkScheduleService:
    @staticmethod
    def get_all_schedules_query():
        """Query base ottimizzata per liste e filtri dinamici"""
        return WorkSchedule.query.options(
            # joinedload(WorkSchedule.user),
            joinedload(WorkSchedule.schedule_type),
            joinedload(WorkSchedule.week_day),
            joinedload(WorkSchedule.work_activity),
            joinedload(WorkSchedule.contract).joinedload(Contract.client)
        )

    @staticmethod
    def get_by_id(schedule_id):
        """Recupera un singolo record con tutte le sue relazioni"""
        return WorkScheduleService.get_all_schedules_query().filter_by(id=schedule_id).first()

    def create_schedule(data):
        # 1. Pulizia stringhe vuote e conversione tipi base
        processed_data = {}
        for key, value in data.items():
            # Se il valore è una stringa vuota, trasformalo in None
            if value == "":
                processed_data[key] = None
            else:
                processed_data[key] = value

        # 2. Conversione specifica per i campi Time
        time_fields = ['start_time', 'end_time']
        for field in time_fields:
            if processed_data.get(field):
                try:
                    # Trasforma "HH:MM" o "HH:MM:SS" in oggetto time
                    time_str = processed_data[field]
                    # Prende solo i primi 5 caratteri se arriva HH:MM:SS
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
    # @staticmethod
    # def create_schedule(data):
    #     new_schedule = WorkSchedule(**data)
    #     db.session.add(new_schedule)
    #     db.session.commit()
    #     return new_schedule

    @staticmethod
    def update_schedule(schedule_id, data):
        schedule = WorkSchedule.query.get(schedule_id)
        if not schedule:
            return None
        
        # Aggiornamento dinamico dei campi passati nel JSON
        for key, value in data.items():
            if hasattr(schedule, key):
                setattr(schedule, key, value)
        
        db.session.commit()
        # Ritorno l'oggetto rinfrescato con le join per il frontend
        return WorkScheduleService.get_by_id(schedule_id)

    @staticmethod
    def delete_schedule(schedule_id):
        schedule = WorkSchedule.query.get(schedule_id)
        if schedule:
            db.session.delete(schedule)
            db.session.commit()
            return True
        return False