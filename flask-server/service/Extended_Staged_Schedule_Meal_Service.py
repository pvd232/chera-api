from .Staged_Schedule_Meal_Service import Staged_Schedule_Meal_Service
from domain.Staged_Schedule_Meal_Domain import Staged_Schedule_Meal_Domain
from domain.Extended_Staged_Schedule_Meal_Domain import (
    Extended_Staged_Schedule_Meal_Domain,
)
from uuid import UUID
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from models import Staged_Schedule_Meal_Model


class Extended_Staged_Schedule_Meal_Service(Staged_Schedule_Meal_Service):
    def get_extended_staged_schedule_meals(
        self, meal_subscription_id: UUID
    ) -> Optional[list["Extended_Staged_Schedule_Meal_Domain"]]:
        staged_schedule_meals: Optional[
            list["Staged_Schedule_Meal_Model"]
        ] = self.staged_schedule_meal_repository.get_staged_schedule_meals(
            meal_subscription_id=meal_subscription_id
        )
        if staged_schedule_meals:
            return [
                Extended_Staged_Schedule_Meal_Domain(staged_schedule_meal_model=x)
                for x in staged_schedule_meals
            ]
        else:
            return None
