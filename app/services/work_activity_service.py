from app.services.base_service import BaseService
from app.models import WorkActivity


class WorkActivityService(BaseService):
    model = WorkActivity