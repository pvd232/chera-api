from .Base_DTO import Base_DTO
from typing import TYPE_CHECKING
from dto.Meal_Plan_DTO import Meal_Plan_DTO

if TYPE_CHECKING:
    from .Nutrient_Daily_Value_DTO import Nutrient_Daily_Value_DTO
    from domain.Meal_Plan_Domain import Meal_Plan_Domain


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
        associated_meal_plan: "Meal_Plan_Domain",
    ):
        self.recipe = recipe
        self.nutrients = nutrients
        self.k_cal = k_cal
        self.protein_k_cal = protein_k_cal
        self.fat_k_cal = fat_k_cal
        self.carb_k_cal = carb_k_cal
        self.weight = weight
        self.associated_meal_plan = Meal_Plan_DTO(meal_plan_domain=associated_meal_plan)
