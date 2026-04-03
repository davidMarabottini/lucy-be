from ..models import User, Role, db
from sqlalchemy.exc import IntegrityError

class UserService:
    @staticmethod
    def create_user(data):
        """Crea un nuovo utente con gestione errori robusta."""
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

    @staticmethod
    def get_all_users():
        """Ritorna la lista completa degli utenti."""
        return User.query.all()

    @staticmethod
    def get_single_user(user_id):
        """Ritorna i dati di un singolo utente"""
        return db.session.get(User, user_id)
    
    @staticmethod
    def update_user(user_id, data):
        """Aggiorna solo i campi inviati (Partial Update)."""
        user = User.query.get(user_id)
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

    @staticmethod
    def delete_user(user_id):
        """Eliminazione fisica dal database."""
        user = User.query.get(user_id)
        if not user:
            return False
        db.session.delete(user)
        db.session.commit()
        return True
