from .Base_DTO import Base_DTO
from typing import TYPE_CHECKING
from dto.Meal_Plan_DTO import Meal_Plan_DTO
from uuid import UUID

if TYPE_CHECKING:
    from .Nutrient_Daily_Value_DTO import Nutrient_Daily_Value_DTO
    from domain.Extended_Meal_Plan_Domain import Extended_Meal_Plan_Domain
    from dto.Extended_Meal_Plan_DTO import Extended_Meal_Plan_DTO


class Food_Nutrient_Stats_DTO(Base_DTO):
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
    ):
        self.meal_plan_id = (meal_plan_id,)
        self.recipe = recipe
        self.nutrients = nutrients
        self.k_cal = k_cal
        self.protein_k_cal = protein_k_cal
        self.fat_k_cal = fat_k_cal
        self.carb_k_cal = carb_k_cal
        self.weight = weight

    def serialize(self):
        serialized_attributes = super().serialize()
        serialized_nutrients = []
        for nutrient in self.nutrients:
            serialized_nutrient = nutrient.serialize()
            serialized_nutrients.append(serialized_nutrient)
        serialized_attributes["nutrients"] = serialized_nutrients

        return serialized_attributes
