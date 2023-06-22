from uuid import UUID
from typing import TYPE_CHECKING
from .Base_DTO import Base_DTO

if TYPE_CHECKING:
    from domain.Meal_Plan_Snack_Domain import Meal_Plan_Snack_Domain


class Meal_Plan_Snack_DTO(Base_DTO):
    def __init__(
        self,
        meal_plan_snack_json: dict = None,
        meal_plan_snack_domain: "Meal_Plan_Snack_Domain" = None,
    ) -> None:
        if meal_plan_snack_json:
            self.id: UUID = UUID(meal_plan_snack_json["id"])
            self.snack_id: UUID = UUID(meal_plan_snack_json["snack_id"])
            self.meal_plan_id: UUID = UUID(meal_plan_snack_json["meal_plan_id"])
            if "multiplier" in meal_plan_snack_json:
                self.multiplier: float = meal_plan_snack_json["multiplier"]
            else:
                self.multiplier: float = 1.0
            self.active: bool = meal_plan_snack_json["active"]
        elif meal_plan_snack_domain:
            self.id: UUID = meal_plan_snack_domain.id
            self.snack_id: UUID = meal_plan_snack_domain.snack_id
            self.meal_plan_id: UUID = meal_plan_snack_domain.meal_plan_id
            self.multiplier: float = meal_plan_snack_domain.multiplier
            self.active: bool = meal_plan_snack_domain.active
