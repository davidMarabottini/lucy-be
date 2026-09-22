from typing import Optional

from flask import Response
from sqlalchemy import inspect
from sqlalchemy.orm import Query

from app.extension import db
from app.auth.decorators import apply_query_filters, paginated_response
from app.utils.exporters import ExportFormat, export_records


class BaseService:
    """
    Servizio base che centralizza le operazioni CRUD standard.

    Ogni sottoclasse deve definire:
        model: la classe SQLAlchemy del modello (obbligatorio)
        query_options: lista di opzioni joinedload per get_all/get_by_id (opzionale, default: [])
    """
    model = None
    query_options = []
    # Colonne da escludere sempre dall'export (es. campi sensibili come password hash)
    export_exclude_fields: list[str] = []

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if cls.model is None:
            raise TypeError(f"{cls.__name__} deve definire 'model'")

    @classmethod
    def _base_query(cls) -> Query:
        query = cls.model.query
        if cls.query_options:
            query = query.options(*cls.query_options)
        return query

    @classmethod
    @paginated_response
    def get_all(cls) -> Query:
        return cls._base_query()

    @classmethod
    def export(cls, fmt: ExportFormat = ExportFormat.XLSX, filename: Optional[str] = None) -> Response:
        """
        Esporta il risultato di get_all (con gli stessi filtri da query string) nel formato richiesto,
        pronto per essere inviato al frontend come download.
        """
        query = apply_query_filters(cls._base_query(), cls.model)
        items = query.all()
        records = [
            {k: v for k, v in item.to_dict().items() if k not in cls.export_exclude_fields}
            for item in items
        ]
        # Se non ci sono righe, mostra comunque le intestazioni delle colonne fisiche del modello
        columns = None
        if not records:
            mapper = inspect(cls.model)
            columns = [c.key for c in mapper.column_attrs if c.key not in cls.export_exclude_fields]
        export_filename = filename or cls.model.__tablename__
        return export_records(records, fmt=fmt, filename=export_filename, columns=columns)

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
    def bulk_update(cls, items_data):
        """
        Aggiorna massivamente una lista di entità in un'unica transazione.
        Ogni elemento in items_data deve contenere la chiave 'id'.
        """
        updated_ids = []

        try:
            for item in items_data:
                entity_id = item.get('id')
                if not entity_id:
                    raise ValueError("Ogni elemento del payload deve contenere il campo 'id'")

                entity = db.session.get(cls.model, entity_id)
                if not entity:
                    raise ValueError(f"Risorsa {cls.model.__name__} con ID {entity_id} non trovata")

                cls._apply_updates(entity, item)
                updated_ids.append(entity.id)

            db.session.commit()

            if cls.query_options:
                return (
                    cls.model.query.filter(cls.model.id.in_(updated_ids))
                    .options(*cls.query_options)
                    .all()
                )

            return [db.session.get(cls.model, eid) for eid in updated_ids]

        except Exception as e:
            db.session.rollback()
            raise e

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
