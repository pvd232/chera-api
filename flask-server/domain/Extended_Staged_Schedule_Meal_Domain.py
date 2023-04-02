from .Staged_Schedule_Meal_Domain import Staged_Schedule_Meal_Domain
from dto.Extended_Meal_DTO import Extended_Meal_DTO
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models import Staged_Schedule_Meal_Model


class Extended_Staged_Schedule_Meal_Domain(Staged_Schedule_Meal_Domain):
    def __init__(self, staged_schedule_meal_model: 'Staged_Schedule_Meal_Model') -> None:
        super().__init__(staged_schedule_meal_object=staged_schedule_meal_model)
        self.associated_meal = Extended_Meal_DTO(
            extended_meal_domain=staged_schedule_meal_model.associated_meal)
