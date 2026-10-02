from flask import Blueprint, session, jsonify, request

cur_company_bp = Blueprint('session_cur_company_bp', __name__)

@cur_company_bp.route('/api/cur-company', methods=['PUT'])
def set_cur_company():
    data = request.get_json()
    cur_company_id = data.get('cur_company_id')
    
    if not cur_company_id:
        return jsonify({'error': 'cur_company_id obbligatorio'}), 400
    
    session.permanent = True
    session['cur_company_id'] = int(cur_company_id)
    return jsonify({'message': f'Cur Company {cur_company_id} selezionata con successo', 'cur_company_id': cur_company_id})

@cur_company_bp.route('/api/cur-company', methods=['GET'])
def get_cur_company():
    cur_company_id = session.get('cur_company_id')
    return jsonify({'cur_company_id': cur_company_id})