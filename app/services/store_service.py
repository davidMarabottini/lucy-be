from app.services.base_service import BaseService
from app.models import Store


class StoreService(BaseService):
    model = Store
