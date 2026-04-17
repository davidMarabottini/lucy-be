from sqlalchemy import inspect
from app.extension import db
from app.auth.decorators import paginated_response


class BaseService:
    """
    Servizio base che centralizza le operazioni CRUD standard.

    Ogni sottoclasse deve definire:
        model: la classe SQLAlchemy del modello (obbligatorio)
        query_options: lista di opzioni joinedload per get_all/get_by_id (opzionale, default: [])
    """
    model = None
    query_options = []

    @classmethod
    @paginated_response
    def get_all(cls):
        query = cls.model.query
        if cls.query_options:
            query = query.options(*cls.query_options)
        return query

    @classmethod
    def get_by_id(cls, entity_id):
        if cls.query_options:
            return cls.model.query.options(*cls.query_options).filter_by(id=entity_id).first()
        return db.session.get(cls.model, entity_id)

    @classmethod
    def create(cls, data):
        filtered = cls._filter_columns(data)
        entity = cls.model(**filtered)
        db.session.add(entity)
        db.session.commit()
        return entity

    @classmethod
    def update(cls, entity_id, data):
        entity = db.session.get(cls.model, entity_id)
        if not entity:
            return None
        cls._apply_updates(entity, data)
        db.session.commit()
        return entity

    @classmethod
    def delete(cls, entity_id):
        entity = db.session.get(cls.model, entity_id)
        if not entity:
            return False
        db.session.delete(entity)
        db.session.commit()
        return True

    @classmethod
    def _filter_columns(cls, data):
        """Filtra il payload mantenendo solo le colonne fisiche del modello, escludendo 'id'."""
        mapper = inspect(cls.model)
        valid_columns = {c.key for c in mapper.column_attrs}
        return {k: v for k, v in data.items() if k in valid_columns and k != 'id'}

    @classmethod
    def _apply_updates(cls, entity, data):
        """Applica gli aggiornamenti parziali. Override per logica custom."""
        mapper = inspect(cls.model)
        valid_columns = {c.key for c in mapper.column_attrs}
        for key, value in data.items():
            if key in valid_columns and key != 'id':
                setattr(entity, key, value)
