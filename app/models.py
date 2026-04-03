from app.baseModel import BaseModel

from . import db
from werkzeug.security import generate_password_hash, check_password_hash

# Associazioni utenti/ruoli
user_roles = db.Table(
    'user_roles',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id')),
    db.UniqueConstraint('user_id', 'role_id', name='unique_user_role')
)

# Ruoli
class Role(db.Model, BaseModel):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

# Utenti
class User(db.Model, BaseModel):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(50))
    surname = db.Column(db.String(50))
    gender = db.Column(db.String(20))
    password_hash = db.Column(db.String(255), nullable=False)
    roles = db.relationship('Role', secondary=user_roles, backref=db.backref('users', lazy='dynamic'))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Clienti
class Client(db.Model, BaseModel):
    __tablename__ = 'clients'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120))
    phone = db.Column(db.String(50))
    
# Giorni della settimana
class WeekDay(db.Model, BaseModel):
    __tablename__ = 'week_days'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, unique=True)

# Tipi di orario
class WorkScheduleType(db.Model, BaseModel):
    __tablename__ = 'work_schedule_types'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    
    # Parametri di Controllo
    frequency = db.Column(db.Integer, nullable=True)
    period = db.Column(db.Enum('DAY', 'WEEK', 'MONTH', 'YEAR', 'FIXED', 'NONE', name='period_types'), default='NONE')

    # Frontend Visual
    icon_name = db.Column(db.String(50), default='Clock') # Nome icona Lucide (es: 'Home', 'Zap')

# Attività specifiche (per day/task)
class WorkActivity(db.Model, BaseModel):
    __tablename__ = 'work_activities'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)


# Tabella di associazione (Ponte)
company_sectors = db.Table(
    'company_sectors',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('company_id', db.Integer, db.ForeignKey('group_companies.id', ondelete='CASCADE')),
    db.Column('sector_id', db.Integer, db.ForeignKey('sectors.id', ondelete='CASCADE')),
    db.UniqueConstraint('company_id', 'sector_id', name='unique_company_sector')
)

class Sector(db.Model, BaseModel):
    __tablename__ = 'sectors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    description = db.Column(db.String(255), nullable=True)


class GroupCompany(db.Model, BaseModel):
    __tablename__ = 'group_companies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    vat_number = db.Column(db.String(20))
    
    # Relazione Many-to-Many
    sectors = db.relationship('Sector', secondary=company_sectors, backref=db.backref('companies', lazy='dynamic'))
    
class Contract(db.Model, BaseModel):
    __tablename__ = 'contracts'
    id = db.Column(db.Integer, primary_key=True)
    contract_code = db.Column(db.String(50), unique=True, nullable=False)
    # FK verso la vostra società che eroga il servizio
    provider_company_id = db.Column(db.Integer, db.ForeignKey('group_companies.id'), nullable=False)
    # FK verso il cliente esterno
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    
    description = db.Column(db.Text, nullable=True)
    
    provider_company = db.relationship('GroupCompany', backref=db.backref('contracts', lazy='dynamic'))
    client = db.relationship('Client', backref=db.backref('contracts', lazy='dynamic'))
    
class WorkSchedule(db.Model, BaseModel):
    __tablename__ = 'work_schedules'
    id = db.Column(db.Integer, primary_key=True)
    
    # Adesso puntiamo al CONTRATTO, non più direttamente al cliente
    contract_id = db.Column(db.Integer, db.ForeignKey('contracts.id'), nullable=False)
    # user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    schedule_type_id = db.Column(db.Integer, db.ForeignKey('work_schedule_types.id'), nullable=False)
    work_activity_id = db.Column(db.Integer, db.ForeignKey('work_activities.id'), nullable=True)
    note = db.Column(db.Text, nullable=True)

    # Orario giornaliero o monte ore
    week_day_id = db.Column(db.Integer, db.ForeignKey('week_days.id'), nullable=True)
    start_time = db.Column(db.Time, nullable=True)
    end_time = db.Column(db.Time, nullable=True)
    weekly_hours = db.Column(db.Float, nullable=True)

    # Relationships
    contract = db.relationship('Contract', backref=db.backref('schedules', lazy='dynamic'))
    # user = db.relationship('User', backref=db.backref('work_schedules', lazy='dynamic'))
    schedule_type = db.relationship('WorkScheduleType', backref=db.backref('work_schedules', lazy='dynamic'))
    week_day = db.relationship('WeekDay', backref=db.backref('work_schedules', lazy='dynamic'))
    work_activity = db.relationship('WorkActivity', backref=db.backref('work_schedules', lazy='dynamic'))
    
    def to_dict(self, seen_ids=None):
        # Richiamiamo la logica base per le colonne e le relazioni caricate
        data = super().to_dict(seen_ids=seen_ids)
        
        # Override specifico per i campi Time: trasformiamo in stringa HH:MM
        if self.start_time:
            data['start_time'] = self.start_time.strftime("%H:%M")
        
        if self.end_time:
            data['end_time'] = self.end_time.strftime("%H:%M")
            
        return data