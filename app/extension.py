from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import inspect


class BaseModel:
    def to_dict(self, seen_ids=None):
        if seen_ids is None:
            seen_ids = set()

        obj_id = (self.__class__.__name__, getattr(self, 'id', id(self)))
        if obj_id in seen_ids:
            return {"id": getattr(self, 'id', None)}

        seen_ids.add(obj_id)

        data = {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

        for key, value in self.__dict__.items():
            if key.startswith('_'):
                continue

            if hasattr(value, 'to_dict'):
                data[key] = value.to_dict(seen_ids=seen_ids.copy())
            elif isinstance(value, list):
                if value and hasattr(value[0], 'to_dict'):
                    data[key] = [item.to_dict(seen_ids=seen_ids.copy()) for item in value]
                elif not value:
                    data[key] = []

        return data

    def __repr__(self):
        class_name = self.__class__.__name__
        obj_id = getattr(self, 'id', 'N/A')
        display_name = ""
        for field in ['name', 'contract_code', 'username', 'email']:
            if hasattr(self, field):
                display_name = f" {field}='{getattr(self, field)}'"
                break
        return f"<{class_name} id={obj_id}{display_name}>"


db = SQLAlchemy(model_class=BaseModel)
migrate = Migrate()