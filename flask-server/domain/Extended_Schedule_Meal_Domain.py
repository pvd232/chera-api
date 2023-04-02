from .Schedule_Meal_Domain import Schedule_Meal_Domain
from domain.Extended_Meal_Domain import Extended_Meal_Domain
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models import Schedule_Meal_Model


class Extended_Schedule_Meal_Domain(Schedule_Meal_Domain):
    def __init__(self, schedule_meal_model: 'Schedule_Meal_Model') -> None:
        super().__init__(schedule_meal_object=schedule_meal_model)
        self.associated_meal = Extended_Meal_Domain(
            meal_model=schedule_meal_model.associated_meal)
