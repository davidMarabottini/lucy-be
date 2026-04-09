from flask import Blueprint, request, jsonify
from ..services.sector_service import SectorService

sectors_bp = Blueprint('sectors_bp', __name__, url_prefix="/api/sectors")

@sectors_bp.route('', methods=['GET'])
def get_sectors():
    sectors = SectorService.get_all()
    return jsonify(sectors), 200

@sectors_bp.route('/<int:sector_id>', methods=['GET'])
def get_sector(sector_id):
    sector = SectorService.get_by_id(sector_id)
    if not sector:
        return jsonify({"error": "Settore non trovato"}), 404
    return jsonify(sector.to_dict()), 200

@sectors_bp.route('', methods=['POST'])
def create_sector():
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({"error": "Il nome è obbligatorio"}), 400
    
    new_sector = SectorService.create(data)
    return jsonify(new_sector.to_dict()), 201

@sectors_bp.route('/<int:sector_id>', methods=['PUT'])
def update_sector(sector_id):
    data = request.get_json()
    updated_sector = SectorService.update(sector_id, data)
    if not updated_sector:
        return jsonify({"error": "Settore non trovato"}), 404
    return jsonify(updated_sector.to_dict()), 200

@sectors_bp.route('/<int:sector_id>', methods=['DELETE'])
def delete_sector(sector_id):
    success = SectorService.delete(sector_id)
    if not success:
        return jsonify({"error": "Settore non trovato o collegato a società"}), 404
    return jsonify({"message": "Settore eliminato con successo"}), 200