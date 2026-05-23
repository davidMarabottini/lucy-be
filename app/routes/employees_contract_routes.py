from flask import Blueprint, request, jsonify
from app.services.employee_contract_service import EmployeeContractService
from sqlalchemy.exc import IntegrityError

employee_contracts_bp = Blueprint("employee_contracts", __name__, url_prefix="/api/employee-contracts")


def _assignment_to_dict(a):
    return {
        "id": a.id,
        "employee_id": a.employee_id,
        "contract_id": a.contract_id,
        "start_date": a.start_date.isoformat(),
        "end_date": a.end_date.isoformat() if a.end_date else None,
    }


@employee_contracts_bp.route("", methods=["POST"])
# @requires_auth
def create_employee_contract():
    data = request.get_json() or {}

    required_fields = ["employee_id", "contract_id", "start_date"]
    missing = [field for field in required_fields if field not in data]
    if missing:
        return jsonify({"error": f"Campi obbligatori mancanti: {', '.join(missing)}"}), 400

    employee_ids = data["employee_id"]
    if not isinstance(employee_ids, list):
        employee_ids = [employee_ids]

    try:
        assignments = EmployeeContractService.bulk_create(
            contract_id=data["contract_id"],
            employee_ids=employee_ids,
            start_date=data["start_date"],
            end_date=data.get("end_date"),
        )
        return jsonify([_assignment_to_dict(a) for a in assignments]), 201

    except IntegrityError:
        return jsonify({"error": "Assegnazione già esistente o ID (Employee/Contract) non valido."}), 400

    except ValueError:
        return jsonify({"error": "Formato data non valido."}), 400