from flask import Blueprint, request, jsonify
from app.services.employees_service import EmployeeService
from ..auth.decorators import requires_auth

employees_bp = Blueprint("employees", __name__, url_prefix="/api/employees")

@employees_bp.route("", methods=["GET"])
# @requires_auth
def list_employees():
    employees = EmployeeService.get_all()
    return jsonify(employees), 200


@employees_bp.route("/<int:employee_id>", methods=["GET"])
# @requires_auth
def get_employee(employee_id):
    employee = EmployeeService.get_by_id(employee_id)
    if not employee:
        return jsonify({"error": "Not found"}), 404

    return jsonify({
        "id": employee.id,
        "name": employee.name,
        "email": employee.email,
        "phone": employee.phone
    })

@employees_bp.route("", methods=["POST"])
# @requires_auth
def create_employee():
    data = request.get_json()
    employee = EmployeeService.create(data)
    return jsonify({"id": employee.id}), 201

@employees_bp.route("/<int:employee_id>", methods=["DELETE"])
# @requires_auth
def delete_employee(employee_id):
    isDeleted = EmployeeService.delete(employee_id)
    return jsonify({"success": isDeleted})


@employees_bp.route("/sync-libemax", methods=["POST"])
# @requires_auth
def sync_libemax():
    try:
        synced = EmployeeService.sync_from_libemax()
        return jsonify({"success": True, "synced": synced}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 502
    