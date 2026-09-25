from flask import Blueprint, request, jsonify
from app.services.employees_service import EmployeeService
from app.services.work_schedule_type_service import WorkScheduleTypeService
from app.services.client_service import ClientService
from app.services.work_activity_service import WorkActivityService
from app.services.group_company_service import GroupCompanyService
from app.services.contract_service import ContractService
from app.services.sector_service import SectorService

from app.utils.exporters import resolve_export_format
from ..auth.decorators import requires_auth

home_bp = Blueprint("home", __name__, url_prefix="/api/home")

# mi serve un servizio che chiami il count di tutte le rotte e torni un json con {sezione: count}
@home_bp.route("/count", methods=["GET"])
@requires_auth
def count_home():
    counts = {
        "CLIENTS": ClientService.count(),
        "EMPLOYEES": EmployeeService.count(),
        "GROUP_COMPANIES": GroupCompanyService.count(),
        "CONTRACTS": ContractService.count(),
        "WORK_ACTIVITIES": WorkActivityService.count(),
        "SECTORS": SectorService.count(),
        "USERS": EmployeeService.count(),
        "WORK_SCHEDULE_TYPES": WorkScheduleTypeService.count(),
    }
    return jsonify(counts), 200
