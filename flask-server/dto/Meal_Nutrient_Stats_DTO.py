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
        recipe: list[str],
        nutrients: list["Nutrient_Daily_Value_DTO"],
        k_cal: float,
        protein_k_cal: float,
        fat_k_cal: float,
        carb_k_cal: float,
        grams: float,
        meal_time: str,
    ):
        super().__init__(
            food_id=food_id,
            food_name=food_name,
            meal_plan_id=meal_plan_id,
            recipe=recipe,
            nutrients=nutrients,
            k_cal=k_cal,
            protein_k_cal=protein_k_cal,
            fat_k_cal=fat_k_cal,
            carb_k_cal=carb_k_cal,
            grams=grams,
        )
        self.meal_time = meal_time
