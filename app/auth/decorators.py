from functools import wraps
from flask import request, jsonify, g
from ..services.auth_service import AuthService
from ..models import User
from sqlalchemy import inspect, or_

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get('authToken')
        if not token:
            return jsonify({"message": "Token mancante"}), 401
        
        user_id = AuthService.decode_token(token)
        if not user_id:
            return jsonify({"message": "Token invalido o scaduto"}), 401
        
        user = User.query.get(user_id)
        if not user:
            return jsonify({"message": "Utente non trovato"}), 401
            
        g.current_user = user
        
        return f(*args, **kwargs)
    return decorated


from functools import wraps
from flask import request, jsonify
from sqlalchemy import inspect, String, Text
from sqlalchemy.orm import Query


def apply_query_filters(query: Query, model, ignored_params: set[str] = frozenset({'page', 'per_page', 'raw', 'format'})) -> Query:
    """Applica alla query i filtri dinamici basati sulla Query String (?name=Libemax)."""
    mapper = inspect(model)
    # Prendiamo solo le colonne reali (escludendo le relazioni per i filtri URL)
    columns = [c.key for c in mapper.column_attrs]

    for key, value in request.args.items():
        if key in ignored_params or not value:
            continue

        if key in columns:
            column_attr = getattr(model, key)

            # Ricerca parziale per stringhe, esatta per il resto (ID, numeri, ecc.)
            if isinstance(column_attr.type, (String, Text)):
                query = query.filter(column_attr.ilike(f"%{value}%"))
            else:
                query = query.filter(column_attr == value)

    return query


def paginated_response(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # 1. Ottieni la query base dal Service
        query = func(*args, **kwargs)

        # 2. Identifica il modello e applica i filtri dinamici
        model = query.column_descriptions[0]['entity']
        query = apply_query_filters(query, model)

        # 3. Parametri di paginazione
        page = request.args.get('page', type=int)
        per_page = request.args.get('per_page', default=10, type=int)
        raw = request.args.get('raw', default='false').lower() == 'true'

        # Ritorno Raw (Senza metadati di paginazione)
        if page is None or raw:
            items = query.all()
            return [i.to_dict() for i in items]

        # Ritorno Paginato Standard
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)

        return {
            "items": [i.to_dict() for i in pagination.items],
            "total": pagination.total,
            "page": pagination.page,
            "pages": pagination.pages,
            "has_next": pagination.has_next,
            "has_prev": pagination.has_prev
        }
    return wrapper
