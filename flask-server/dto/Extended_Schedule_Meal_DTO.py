from dto.Schedule_Meal_DTO import Schedule_Meal_DTO
from dto.Extended_Meal_DTO import Extended_Meal_DTO
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from domain.Extended_Schedule_Meal_Domain import Extended_Schedule_Meal_Domain


class Extended_Schedule_Meal_DTO(Schedule_Meal_DTO):
    def __init__(self, extended_schedule_meal_domain: 'Extended_Schedule_Meal_Domain' = None) -> None:
        super().__init__(schedule_meal_domain=extended_schedule_meal_domain)
        self.associated_meal = Extended_Meal_DTO(
            extended_meal_domain=extended_schedule_meal_domain.associated_meal)
