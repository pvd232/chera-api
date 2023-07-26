from .Food_Nutrient_Stats_DTO import Food_Nutrient_Stats_DTO
from uuid import UUID
from typing import TYPE_CHECKING
from dto.Snack_DTO import Snack_DTO

if TYPE_CHECKING:
    from domain.Snack_Domain import Snack_Domain
    from domain.Extended_Meal_Plan_Domain import Extended_Meal_Plan_Domain
    from .Nutrient_Daily_Value_DTO import Nutrient_Daily_Value_DTO


class Snack_Nutrient_Stats_DTO(Food_Nutrient_Stats_DTO):
    def __init__(
        self,
        meal_plan_id: UUID,
        recipe: list[str],
        nutrients: list["Nutrient_Daily_Value_DTO"],
        k_cal: float,
        protein_k_cal: float,
        fat_k_cal: float,
        carb_k_cal: float,
        weight: float,
        associated_snack: "Snack_Domain",
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
        self.associated_snack = Snack_DTO(snack_domain=associated_snack)
    