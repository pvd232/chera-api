from .Schedule_Meal_Service import Schedule_Meal_Service
from domain.Extended_Schedule_Meal_Domain import Extended_Schedule_Meal_Domain
from uuid import UUID
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from models import Schedule_Meal_Model
    from service.Client_Service import Client_Service


class Extended_Schedule_Meal_Service(Schedule_Meal_Service):
    def get_extended_schedule_meals(self, meal_subscription_id: UUID) -> Optional[list['Extended_Schedule_Meal_Domain']]:
        schedule_meals: Optional[list['Schedule_Meal_Model']
                                 ] = self.schedule_meal_repository.get_schedule_meals(meal_subscription_id=meal_subscription_id)
        if schedule_meals:
            return [Extended_Schedule_Meal_Domain(schedule_meal_object=x) for x in schedule_meals]
        else:
            return None

    def get_dietitian_extended_schedule_meals(self, dietitian_id: str, client_service: 'Client_Service') -> Optional[list['Extended_Schedule_Meal_Domain']]:
        schedule_meals: Optional[list['Schedule_Meal_Model']
                                 ] = self.schedule_meal_repository.get_dietitian_schedule_meals(dietitian_id=dietitian_id, client_repository=client_service.client_repository)
        if schedule_meals:
            return [Extended_Schedule_Meal_Domain(schedule_meal_model=x) for x in schedule_meals]
        else:
            return None
