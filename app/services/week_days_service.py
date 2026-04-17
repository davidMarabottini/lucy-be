from app.services.base_service import BaseService
from app.models import WeekDay


class WeekDaysService(BaseService):
    model = WeekDay
    
