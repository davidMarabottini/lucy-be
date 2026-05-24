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


@employee_contracts_bp.route("/by-contract/<int:contract_id>", methods=["GET"])
# @requires_auth
def get_employees_by_contract(contract_id):
    target_date = request.args.get("date")

    try:
        assignments = EmployeeContractService.get_employees_by_contract_and_date(
            contract_id=contract_id,
            target_date=target_date,
        )
    except ValueError:
        return jsonify({"error": "Formato data non valido. Usa YYYY-MM-DD."}), 400

    result = []
    for a in assignments:
        emp = a.employee
        result.append({
            "assignment_id": a.id,
            "start_date": a.start_date.isoformat(),
            "end_date": a.end_date.isoformat() if a.end_date else None,
            "employee": {
                "id": emp.id,
                "name": emp.name,
                "surname": emp.surname,
                "email": emp.email,
                "phone": emp.phone,
                "libemax_id": emp.libemax_id,
            },
        })

    return jsonify(result), 200

@employee_contracts_bp.route("/<int:assignment_id>", methods=["PATCH"])
# @requires_auth
def update_employee_contract(assignment_id):
    data = request.get_json() or {}

    if not data:
        return jsonify({"error": "Nessun dato fornito."}), 400

    for locked in ("id", "employee_id", "contract_id"):
        data.pop(locked, None)

    try:
        assignment = EmployeeContractService.update(assignment_id, data)
    except ValueError:
        return jsonify({"error": "Formato data non valido."}), 400

    if assignment is None:
        return jsonify({"error": "Assegnazione non trovata."}), 404

    return jsonify(_assignment_to_dict(assignment)), 200