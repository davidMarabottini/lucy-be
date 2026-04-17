from app.services.base_service import BaseService
from app.models import Sector


class SectorService(BaseService):
    model = Sector