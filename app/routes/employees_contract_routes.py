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
        from app import db
        db.session.rollback()
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

@employee_contracts_bp.route("/by-employee/<int:employee_id>", methods=["GET"])
# @requires_auth
def get_contracts_by_employee(employee_id):
    target_date = request.args.get("date")

    try:
        assignments = EmployeeContractService.get_contracts_by_employee(
            employee_id=employee_id,
            target_date=target_date,
        )
    except ValueError:
        return jsonify({"error": "Formato data non valido. Usa YYYY-MM-DD."}), 400

    result = []
    for a in assignments:
        contract = a.contract
        client = contract.client
        schedules = contract.schedules.all()

        result.append({
            "assignment_id": a.id,
            "assignment_start_date": a.start_date.isoformat(),
            "assignment_end_date": a.end_date.isoformat() if a.end_date else None,
            "contract": {
                "id": contract.id,
                "contract_code": contract.contract_code,
                "start_date": contract.start_date.isoformat() if contract.start_date else None,
                "end_date": contract.end_date.isoformat() if contract.end_date else None,
                "description": contract.description,
                "client": {
                    "id": client.id,
                    "name": client.name,
                    "email": client.email,
                    "phone": client.phone,
                },
                "work_schedules": [
                    {
                        "id": s.id,
                        "note": s.note,
                        "start_time": s.start_time.strftime("%H:%M") if s.start_time else None,
                        "end_time": s.end_time.strftime("%H:%M") if s.end_time else None,
                        "weekly_hours": s.weekly_hours,
                        "schedule_type": {
                            "id": s.schedule_type.id,
                            "name": s.schedule_type.name,
                            "icon_name": s.schedule_type.icon_name,
                        } if s.schedule_type else None,
                        "week_day": {
                            "id": s.week_day.id,
                            "name": s.week_day.name,
                        } if s.week_day else None,
                        "work_activity": {
                            "id": s.work_activity.id,
                            "name": s.work_activity.name,
                        } if s.work_activity else None,
                    }
                    for s in schedules
                ],
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