from ..extension import db
from ..models import User, Role, WeekDay


def ensure_roles():
    admin = Role.query.filter_by(name="admin").first()
    user = Role.query.filter_by(name="user").first()
    if not admin:
        admin = Role(name="admin")
    if not user:
        user = Role(name="user")
    db.session.add_all([admin, user])
    db.session.commit()
    return admin, user


def create_admin(username, email, password):
    admin_role, user_role = ensure_roles()
    if User.query.filter_by(email=email).first():
        return "Errore: Email già esistente."
    user = User(username=username, email=email, name="Admin")
    user.set_password(password)
    user.roles.extend([admin_role, user_role])
    db.session.add(user)
    db.session.commit()
    return f"Admin '{username}' creato."


def create_week_days():
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    new_days = [WeekDay(name=d) for d in days if not WeekDay.query.filter_by(name=d).first()]
    if new_days:
        db.session.add_all(new_days)
        db.session.commit()
        return f"Creati {len(new_days)} giorni."
    return "Già presenti."
