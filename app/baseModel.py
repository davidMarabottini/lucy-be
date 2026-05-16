# BaseModel is defined in app.extension and injected into SQLAlchemy as model_class.
# This re-export exists only for backwards compatibility.
from app.extension import BaseModel

__all__ = ["BaseModel"]

