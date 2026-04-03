from flask import Blueprint, jsonify, request
import datetime
import random

libemax_bp = Blueprint("libemax", __name__, url_prefix="/api/libemax")

# ---- Tutti gli utenti con dettagli aggiuntivi ----
@libemax_bp.route("/users", methods=["GET"])
def get_users():
    users = [
        {"id": 1, "name": "Mario Rossi", "email": "m.rossi@example.com",
         "phone": "333-1234567", "theoretical_hours": 8, "total_hours": 7.5},
        {"id": 2, "name": "Luigi Bianchi", "email": "l.bianchi@example.com",
         "phone": "333-2345678", "theoretical_hours": 8, "total_hours": None},
        {"id": 3, "name": "Anna Verdi", "email": "a.verdi@example.com",
         "phone": "333-3456789", "theoretical_hours": 6, "total_hours": 5.5},
    ]
    return jsonify(users)

# ---- Tutti i clienti con indirizzo ----
@libemax_bp.route("/clients", methods=["GET"])
def get_clients():
    clients = [
        {"id": 1, "name": "Cliente A", "address": "Via Milano 10, Roma"},
        {"id": 2, "name": "Cliente B", "address": "Piazza Duomo 5, Milano"},
        {"id": 3, "name": "Cliente C", "address": "Corso Torino 22, Torino"},
    ]
    return jsonify(clients)

# ---- Utenti che dovrebbero essere al lavoro ma non hanno timbrato (con telefono) ----
@libemax_bp.route("/missing_clockin", methods=["GET"])
def missing_clockin():
    missing = [
        {"id": 1, "name": "Mario Rossi", "expected_time": "09:00", "phone": "333-1234567", "delay": 2},
        {"id": 3, "name": "Anna Verdi", "expected_time": "09:00", "phone": "333-3456789", "delay": 2},
    ]
    return jsonify(missing)

# ---- Utenti che hanno timbrato lontano dal luogo di lavoro ----
@libemax_bp.route("/remote_clockin", methods=["GET"])
def remote_clockin():
    remote = [
        {"id": 2, "name": "Luigi Bianchi", "time": "09:15", "location": "Via Roma 123, Milano", "distance": 3},
    ]
    return jsonify(remote)

# ---- Dettagli di un singolo cliente/condominio ----
@libemax_bp.route("/clients/<int:client_id>", methods=["GET"])
def client_details(client_id: int):
    clients = {
        1: {"id": 1, "name": "Cliente A", "address": "Via Milano 10, Roma",
            "phone": "06-1234567", "email": "clientea@example.com", "hours": 40,
            "schedule": "09:00-17:00"},
        2: {"id": 2, "name": "Cliente B", "address": "Piazza Duomo 5, Milano",
            "phone": "02-2345678", "email": "clienteb@example.com", "hours": 35,
            "schedule": "08:00-15:00"},
        3: {"id": 3, "name": "Cliente C", "address": "Corso Torino 22, Torino",
            "phone": "011-3456789", "email": "clientec@example.com", "hours": None,
            "schedule": None},
    }
    client = clients.get(client_id)
    if not client:
        return jsonify({"error": "Client not found"}), 404
    return jsonify(client)

# from flask import Blueprint, jsonify
# import datetime
# import random

# libemax_bp = Blueprint("libemax", __name__, url_prefix="/api/libemax")

# # ---- Tutti gli utenti ----
# @libemax_bp.route("/users", methods=["GET"])
# def get_users():
#     users = [
#         {"id": 1, "name": "Mario Rossi", "email": "m.rossi@example.com"},
#         {"id": 2, "name": "Luigi Bianchi", "email": "l.bianchi@example.com"},
#         {"id": 3, "name": "Anna Verdi", "email": "a.verdi@example.com"},
#     ]
#     return jsonify(users)

# # ---- Tutti i clienti ----
# @libemax_bp.route("/clients", methods=["GET"])
# def get_clients():
#     clients = [
#         {"id": 1, "name": "Cliente A"},
#         {"id": 2, "name": "Cliente B"},
#         {"id": 3, "name": "Cliente C"},
#     ]
#     return jsonify(clients)

# # ---- Utenti che dovrebbero essere al lavoro ma non hanno timbrato ----
# @libemax_bp.route("/missing_clockin", methods=["GET"])
# def missing_clockin():
#     missing = [
#         {"id": 1, "name": "Mario Rossi", "expected_time": "09:00"},
#         {"id": 3, "name": "Anna Verdi", "expected_time": "09:00"},
#     ]
#     return jsonify(missing)

# # ---- Utenti che hanno timbrato lontano dal luogo di lavoro ----
# @libemax_bp.route("/remote_clockin", methods=["GET"])
# def remote_clockin():
#     remote = [
#         {"id": 2, "name": "Luigi Bianchi", "time": "09:15", "location": "Via Roma 123, Milano"},
#     ]
#     return jsonify(remote)