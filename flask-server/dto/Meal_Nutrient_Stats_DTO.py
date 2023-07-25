from .Food_Nutrient_Stats_DTO import Food_Nutrient_Stats_DTO
from dto.Extended_Meal_DTO import Extended_Meal_DTO

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from domain.Extended_Meal_Domain import Extended_Meal_Domain
    from domain.Meal_Plan_Domain import Meal_Plan_Domain
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
        associated_meal_plan: "Meal_Plan_Domain",
        associated_meal: "Extended_Meal_Domain",
    ):
        super().__init__(
            recipe=recipe,
            nutrients=nutrients,
            k_cal=k_cal,
            protein_k_cal=protein_k_cal,
            fat_k_cal=fat_k_cal,
            carb_k_cal=carb_k_cal,
            weight=weight,
            associated_meal_plan=associated_meal_plan,
        )
        self.associated_meal = Extended_Meal_DTO(extended_meal_domain=associated_meal)

    def serialize(self):
        serialized_attributes = super().serialize()
        serialized_nutrients = []
        for nutrient in self.nutrients:
            serialized_nutrient = nutrient.serialize()
            serialized_nutrients.append(serialized_nutrient)
        serialized_attributes["nutrients"] = serialized_nutrients

        return serialized_attributes
