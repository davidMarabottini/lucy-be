from flask import Blueprint, request, jsonify
from ..services.group_company_service import GroupCompanyService
from ..auth.decorators import requires_auth

group_company_bp = Blueprint('group_company_bp', __name__, url_prefix="/api/group-company")

@group_company_bp.route('', methods=['GET'])
@requires_auth
def get_companies():
    """Recupera tutte le società del gruppo"""
    companies = GroupCompanyService.get_all()
    print(companies)
    return jsonify(companies), 200
    # return jsonify([c.to_dict() for c in companies]), 200

@group_company_bp.route('/<int:company_id>', methods=['GET'])
@requires_auth
def get_company(company_id):
    """Recupera una singola società per ID"""
    company = GroupCompanyService.get_by_id(company_id)
    if not company:
        return jsonify({"error": "Società non trovata"}), 404
    return jsonify(company.to_dict()), 200

@group_company_bp.route('', methods=['POST'])
@requires_auth
def create_company():
    """Crea una nuova società del gruppo"""
    data = request.get_json()
    
    # Validazione minima: nome e sector_ids sono necessari
    if not data or 'name' not in data or 'sector_ids' not in data:
        return jsonify({"error": "Nome e ID Settore sono obbligatori"}), 400
    
    try:
        new_company = GroupCompanyService.create(data)
        return jsonify(new_company.to_dict()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@group_company_bp.route('/<int:company_id>', methods=['PUT'])
@requires_auth
def update_company(company_id):
    """Aggiorna una società esistente"""
    data = request.get_json()
    updated_company = GroupCompanyService.update(company_id, data)
    if not updated_company:
        return jsonify({"error": "Società non trovata"}), 404
    return jsonify(updated_company.to_dict()), 200

@group_company_bp.route('/<int:company_id>', methods=['DELETE'])
@requires_auth
def delete_company(company_id):
    """Elimina una società"""
    success = GroupCompanyService.delete(company_id)
    if not success:
        return jsonify({"error": "Società non trovata"}), 404
    return jsonify({"message": "Società eliminata con successo"}), 200