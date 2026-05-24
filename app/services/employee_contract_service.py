from app.services.base_service import BaseService
from app.models import Client, EmployeeContract, Employee
from app import db
from datetime import date, datetime

class EmployeeContractService(BaseService):
    model = EmployeeContract

    @staticmethod
    def _parse_date(value):
        if not isinstance(value, str):
            return value
        # Handle ISO 8601 with timezone (e.g. "2026-05-22T22:00:00.000Z")
        if 'T' in value:
            return datetime.fromisoformat(value.replace('Z', '+00:00')).date()
        return datetime.strptime(value, '%Y-%m-%d').date()

    @classmethod
    def create(cls, data):
        payload = data.copy()
        payload['start_date'] = cls._parse_date(payload['start_date'])
        if payload.get('end_date'):
            payload['end_date'] = cls._parse_date(payload['end_date'])
        return super().create(payload)

    @classmethod
    def bulk_create(cls, contract_id, employee_ids, start_date, end_date):
        results = []
        for emp_id in employee_ids:
            payload = {
                'contract_id': contract_id,
                'employee_id': emp_id,
                'start_date': cls._parse_date(start_date),
                'end_date': cls._parse_date(end_date) if end_date else None,
            }
            results.append(super().create(payload))
        return results

    @classmethod
    def get_employees_by_contract_and_date(cls, contract_id, target_date=None):
        if target_date is None:
            target_date = date.today()
        elif isinstance(target_date, str):
            target_date = cls._parse_date(target_date)

        assignments = (
            db.session.query(EmployeeContract)
            .join(Employee, Employee.id == EmployeeContract.employee_id)
            .filter(
                EmployeeContract.contract_id == contract_id,
                EmployeeContract.start_date <= target_date,
                db.or_(
                    EmployeeContract.end_date == None,
                    EmployeeContract.end_date >= target_date,
                ),
            )
            .all()
        )
        return assignments
    
    @classmethod
    def update(cls, assignment_id, data):
        payload = data.copy()
        if 'start_date' in payload:
            payload['start_date'] = cls._parse_date(payload['start_date'])
        if 'end_date' in payload:
            payload['end_date'] = cls._parse_date(payload['end_date']) if payload['end_date'] else None
        return super().update(assignment_id, payload)