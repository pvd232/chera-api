from .Base_DTO import Base_DTO
from uuid import UUID
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .Nutrient_Daily_Value_DTO import Nutrient_Daily_Value_DTO


class Food_Nutrient_Stats_DTO(Base_DTO):
    def __init__(
        self,
        food_id: UUID,
        food_name: str,
        meal_plan_id: UUID,
        nutrients: list["Nutrient_Daily_Value_DTO"],
    ):
        self.food_id = food_id
        self.food_name = food_name
        self.meal_plan_id = meal_plan_id
        self.nutrients = nutrients
