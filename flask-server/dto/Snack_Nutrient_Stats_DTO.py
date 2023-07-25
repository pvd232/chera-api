from .Food_Nutrient_Stats_DTO import Food_Nutrient_Stats_DTO
from uuid import UUID
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from domain.Snack_Domain import Snack_Domain
    from domain.Extended_Meal_Plan_Domain import Extended_Meal_Plan_Domain
    from .Nutrient_Daily_Value_DTO import Nutrient_Daily_Value_DTO
    from dto.Snack_DTO import Snack_DTO


class Snack_Nutrient_Stats_DTO(Food_Nutrient_Stats_DTO):
    def __init__(
        self,
        recipe: list[str],
        nutrients: list["Nutrient_Daily_Value_DTO"],
        k_cal: float,
        protein_k_cal: float,
        fat_k_cal: float,
        carb_k_cal: float,
        weight: float,
        associated_meal_plan: "Extended_Meal_Plan_Domain",
        associated_snack: "Snack_Domain",
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
        self.associated_snack = Snack_DTO(snack_domain=associated_snack)
