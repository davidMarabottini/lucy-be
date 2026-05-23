from app.services.base_service import BaseService
from app.models import EmployeeContract
from datetime import datetime

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