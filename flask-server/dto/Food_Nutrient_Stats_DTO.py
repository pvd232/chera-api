from .Base_DTO import Base_DTO
from uuid import UUID
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .Nutrient_Daily_Value_DTO import Nutrient_Daily_Value_DTO

    # serialized_attributes["k_cal"] = round(self.get_k_cal())
    # serialized_attributes["protein_k_cal"] = round(
    #     self.get_adjusted_protein_k_cal()
    # )
    # serialized_attributes["fat_k_cal"] = round(self.get_adjusted_fat_k_cal())
    # serialized_attributes["carb_k_cal"] = round(self.get_adjusted_carb_k_cal())


class Food_Nutrient_Stats_DTO(Base_DTO):
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
    ):
        self.food_id = food_id
        self.food_name = food_name
        self.meal_plan_id = meal_plan_id
        self.recipe = recipe
        self.nutrients = nutrients
        self.k_cal = k_cal
        self.protein_k_cal = protein_k_cal
        self.fat_k_cal = fat_k_cal
        self.carb_k_cal = carb_k_cal
        self.grams = grams
