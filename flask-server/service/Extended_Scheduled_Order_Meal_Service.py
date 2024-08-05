from .Scheduled_Order_Meal_Service import Scheduled_Order_Meal_Service
from domain.Extended_Scheduled_Order_Meal_Domain import (
    Extended_Scheduled_Order_Meal_Domain,
)
from typing import Optional, TYPE_CHECKING
from uuid import UUID

if TYPE_CHECKING:
    from models import Scheduled_Order_Meal_Model


class Extended_Scheduled_Order_Meal_Service(Scheduled_Order_Meal_Service):
    def get_upcoming_extended_scheduled_order_meals(
        self, meal_subscription_id: Optional[UUID] = None
    ) -> Optional[list["Extended_Scheduled_Order_Meal_Domain"]]:
        scheduled_order_meals: Optional[list["Scheduled_Order_Meal_Model"]] = (
            self.scheduled_order_meal_repository.get_upcoming_scheduled_order_meals(
                meal_subscription_id=meal_subscription_id
            )
        )
        if scheduled_order_meals:
            return [
                Extended_Scheduled_Order_Meal_Domain(scheduled_order_meal_model=x)
                for x in scheduled_order_meals
            ]
        else:
            return None
