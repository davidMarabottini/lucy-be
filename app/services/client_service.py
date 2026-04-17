from app.services.base_service import BaseService
from app.models import Client


class ClientService(BaseService):
    model = Client
