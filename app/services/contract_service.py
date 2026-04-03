
from app.auth.decorators import paginated_response

from ..models import Contract, db
from datetime import datetime
from sqlalchemy.orm import joinedload

class ContractService:
    @staticmethod
    @paginated_response
    def get_all():
        """Recupera tutti i contratti caricando anche i dati delle relazioni"""
        # return Contract.query
        return Contract.query.options(joinedload(Contract.provider_company), joinedload(Contract.client))

    @staticmethod
    @staticmethod
    def get_by_id(contract_id):
        return Contract.query.options(
            joinedload(Contract.provider_company),
            joinedload(Contract.client)
        ).filter(Contract.id == contract_id).first()

    @staticmethod
    def create(data):
        # Gestione date: convertiamo le stringhe ISO in oggetti date
        start_date = data.get("start_date")
        end_date = data.get("end_date")
        
        if isinstance(start_date, str):
            start_date = datetime.fromisoformat(start_date).date()
        if isinstance(end_date, str):
            end_date = datetime.fromisoformat(end_date).date()

        # USARE I NOMI DEFINITI NEL MODELLO DB
        contract = Contract(
            contract_code=data.get("contract_code"), # NO title
            provider_company_id=data.get("group_company_id"), # Allineato al payload frontend
            client_id=data.get("client_id"),
            start_date=start_date,
            end_date=end_date,
            description=data.get("description")
        )
        
        db.session.add(contract)
        db.session.commit()
        return contract

    @staticmethod
    def update(contract_id, data):
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

    @staticmethod
    def delete(contract_id):
        contract = db.session.get(Contract, contract_id)
        if not contract:
            return False
        db.session.delete(contract)
        db.session.commit()
        return True