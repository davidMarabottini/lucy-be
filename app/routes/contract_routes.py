from flask import Blueprint, request, jsonify
from app.services.contract_service import ContractService
from ..auth.decorators import requires_auth

contracts_bp = Blueprint("contracts", __name__, url_prefix="/api/contracts")

@contracts_bp.route("", methods=["GET"])
@requires_auth
def list_contracts():
    contracts = ContractService.get_all()
    return jsonify(contracts), 200

@contracts_bp.route("/<int:contract_id>", methods=["GET"])
@requires_auth
def get_contract(contract_id):
    contract = ContractService.get_by_id(contract_id)
    if not contract:
        return jsonify({"error": "Not found"}), 404

    return jsonify({
        "id": contract.id,
        "contract_code": contract.contract_code,
        "description": contract.description,
        "start_date": contract.start_date.isoformat() if contract.start_date else None,
        "end_date": contract.end_date.isoformat() if contract.end_date else None,
        # Restituiamo piccoli oggetti per le aziende
        "provider": {
            "id": contract.provider_company.id,
            "name": contract.provider_company.name
        } if contract.provider_company else None,
        "client": {
            "id": contract.client.id,
            "name": contract.client.name
        } if contract.client else None
    })

@contracts_bp.route("", methods=["POST"])
@requires_auth
def create_contract():
    data = request.get_json()
    # Il service ora riceverà il payload corretto (contract_code, client_id, ecc.)
    contract = ContractService.create(data)
    return jsonify({"id": contract.id}), 201

@contracts_bp.route("/<int:contract_id>", methods=["DELETE"])
@requires_auth
def delete_contract(contract_id):
    isDeleted = ContractService.delete(contract_id)
    return jsonify({"success": isDeleted})