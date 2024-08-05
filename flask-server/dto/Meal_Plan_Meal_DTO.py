from uuid import UUID
from typing import TYPE_CHECKING, Optional
from .Base_DTO import Base_DTO

if TYPE_CHECKING:
    from domain.Meal_Plan_Meal_Domain import Meal_Plan_Meal_Domain


class Meal_Plan_Meal_DTO(Base_DTO):
    def __init__(
        self,
        meal_plan_meal_json: Optional[dict] = None,
        meal_plan_meal_domain: "Meal_Plan_Meal_Domain" = None,
    ) -> None:
        if meal_plan_meal_json:
            self.id: UUID = UUID(meal_plan_meal_json["id"])
            self.meal_id: UUID = UUID(meal_plan_meal_json["meal_id"])
            self.meal_plan_id: UUID = UUID(meal_plan_meal_json["meal_plan_id"])
            if "multiplier" in meal_plan_meal_json:
                self.multiplier: float = meal_plan_meal_json["multiplier"]
            else:
                self.multiplier: float = 1.0
            self.active: bool = meal_plan_meal_json["active"]
        elif meal_plan_meal_domain:
            self.id: UUID = meal_plan_meal_domain.id
            self.meal_id: UUID = meal_plan_meal_domain.meal_id
            self.meal_plan_id: UUID = meal_plan_meal_domain.meal_plan_id
            self.multiplier: float = meal_plan_meal_domain.multiplier
            self.active: bool = meal_plan_meal_domain.active
