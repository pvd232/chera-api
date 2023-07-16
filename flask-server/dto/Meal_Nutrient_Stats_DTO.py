from .Food_Nutrient_Stats_DTO import Food_Nutrient_Stats_DTO
from uuid import UUID
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .Nutrient_Daily_Value_DTO import Nutrient_Daily_Value_DTO


class Meal_Nutrient_Stats_DTO(Food_Nutrient_Stats_DTO):
    def __init__(
        self,
        food_id: UUID,
        food_name: str,
        meal_plan_id: UUID,
        nutrients: list["Nutrient_Daily_Value_DTO"],
        meal_time: str,
    ):
        super().__init__(
            food_id=food_id,
            food_name=food_name,
            meal_plan_id=meal_plan_id,
            nutrients=nutrients,
        )
        self.meal_time = meal_time
