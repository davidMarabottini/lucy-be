import jwt
import datetime
import os
from flask import make_response, jsonify
from ..models import User, Role, db
from sqlalchemy import or_

class AuthService:
    SECRET_KEY = os.environ["INTERNAL_SECRET_KEY"]
    @staticmethod
    def generate_token(user):
        """Genera un JWT reale con scadenza a 4 ore."""
        #TODO: sostituire con un token più robusto e sicuro in produzione
        #TODO: UTCNOW è deprecato, sostituire con datetime.now(timezone.utc) in futuro
        payload = {
            'user_id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=4),
            'iat': datetime.datetime.utcnow()
        }
        return jwt.encode(payload, AuthService.SECRET_KEY, algorithm='HS256')

    @staticmethod
    def decode_token(token):
        """Decodifica il token e restituisce l'ID utente o None."""
        try:
            payload = jwt.decode(token, AuthService.SECRET_KEY, algorithms=['HS256'])
            return payload['user_id']
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            return None

    @staticmethod
    def login_user(username_or_email, password):
        """
        Logica centrale di login: 
        1. Verifica utente 
        2. Genera Token 
        3. Crea la risposta con Cookie
        """
        user = User.query.filter(
            or_(User.username == username_or_email, User.email == username_or_email)
        ).first()

        if not user or not user.check_password(password):
            return None, "Credenziali non valide"

        token = jwt.encode({
            'user_id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, AuthService.SECRET_KEY, algorithm='HS256')

        user_data = {
            "user": user.username,
            "role": [r.name for r in user.roles]
        }

        response = make_response(jsonify(user_data))
        response.set_cookie(
            'authToken', token,
            httponly=True,
            secure=False,
            samesite='Lax',
            max_age=3600
        )
        return response, None

    @staticmethod
    def logout_user():
        """Semplice reset del cookie."""
        response = make_response(jsonify({"status": "success"}))
        response.set_cookie('authToken', '', expires=0)
        return response

    @staticmethod
    def get_logged_in_user(token):
        """Decodifica e recupera l'oggetto User dal DB."""
        try:
            payload = jwt.decode(token, AuthService.SECRET_KEY, algorithms=['HS256'])
            return User.query.get(payload['user_id'])
        except:
            return None