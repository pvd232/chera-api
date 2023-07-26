from .Food_Nutrient_Stats_DTO import Food_Nutrient_Stats_DTO
from dto.Extended_Meal_DTO import Extended_Meal_DTO
from typing import TYPE_CHECKING
from uuid import UUID

if TYPE_CHECKING:
    from domain.Extended_Meal_Domain import Extended_Meal_Domain
    from .Nutrient_Daily_Value_DTO import Nutrient_Daily_Value_DTO


class Meal_Nutrient_Stats_DTO(Food_Nutrient_Stats_DTO):
    def __init__(
        self,
        recipe: list[str],
        nutrients: list["Nutrient_Daily_Value_DTO"],
        k_cal: float,
        protein_k_cal: float,
        fat_k_cal: float,
        carb_k_cal: float,
        weight: float,
        meal_plan_id: UUID,
        associated_meal: "Extended_Meal_Domain",
    ):
        super().__init__(
            meal_plan_id=meal_plan_id,
            recipe=recipe,
            nutrients=nutrients,
            k_cal=k_cal,
            protein_k_cal=protein_k_cal,
            fat_k_cal=fat_k_cal,
            carb_k_cal=carb_k_cal,
            weight=weight,
        )
        self.associated_meal = Extended_Meal_DTO(extended_meal_domain=associated_meal)
