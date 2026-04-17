from app.services.base_service import BaseService
from app.models import Contract, db
from datetime import datetime
from sqlalchemy.orm import joinedload


class ContractService(BaseService):
    model = Contract
    query_options = [joinedload(Contract.provider_company), joinedload(Contract.client)]

    @classmethod
    def create(cls, data):
        start_date = data.get("start_date")
        end_date = data.get("end_date")
        if isinstance(start_date, str):
            start_date = datetime.fromisoformat(start_date).date()
        if isinstance(end_date, str):
            end_date = datetime.fromisoformat(end_date).date()

        contract = Contract(
            contract_code=data.get("contract_code"),
            provider_company_id=data.get("group_company_id"),
            client_id=data.get("client_id"),
            start_date=start_date,
            end_date=end_date,
            description=data.get("description")
        )
        db.session.add(contract)
        db.session.commit()
        return contract

    @classmethod
    def update(cls, contract_id, data):
        contract = db.session.get(Contract, contract_id)
        if not contract:
            return None
        if "contract_code" in data:
            contract.contract_code = data["contract_code"]
        if "description" in data:
            contract.description = data["description"]
        if "group_company_id" in data:
            contract.provider_company_id = data["group_company_id"]
        if "client_id" in data:
            contract.client_id = data["client_id"]
        if "start_date" in data:
            val = data["start_date"]
            contract.start_date = datetime.fromisoformat(val).date() if isinstance(val, str) else val
        if "end_date" in data:
            val = data["end_date"]
            contract.end_date = datetime.fromisoformat(val).date() if isinstance(val, str) else val
        db.session.commit()
        return contract