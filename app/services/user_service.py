from app.services.base_service import BaseService
from app.models import User, Role, db
from sqlalchemy.exc import IntegrityError


class UserService(BaseService):
    model = User

    @classmethod
    def get_all(cls):
        """Override: ritorna tutti gli utenti senza paginazione."""
        return cls.model.query.all()

    @classmethod
    def create(cls, data):
        """Override: gestisce password e ruoli, ritorna (user, error)."""
        try:
            role_names = data.get('roles', ['user'])
            new_user = User(
                username=data.get('username'),
                email=data.get('email'),
                name=data.get('name'),
                surname=data.get('surname'),
                gender=data.get('gender')
            )
            new_user.set_password(data.get('password'))

            for r_name in role_names:
                role = Role.query.filter_by(name=r_name).first()
                if role:
                    new_user.roles.append(role)

            db.session.add(new_user)
            db.session.commit()
            return new_user, None

        except IntegrityError:
            db.session.rollback()
            return None, "Username o Email già esistenti nel database"
        except Exception as e:
            db.session.rollback()
            return None, str(e)

    @classmethod
    def update(cls, user_id, data):
        """Override: aggiornamento parziale con gestione errori, ritorna (user, error)."""
        user = db.session.get(User, user_id)
        if not user:
            return None, "Utente non trovato"

        if 'name' in data: user.name = data['name']
        if 'surname' in data: user.surname = data['surname']
        if 'gender' in data: user.gender = data['gender']
        if 'email' in data: user.email = data['email']

        if 'password' in data and data['password']:
            user.set_password(data['password'])

        try:
            db.session.commit()
            return user, None
        except IntegrityError:
            db.session.rollback()
            return None, "Email già occupata"
