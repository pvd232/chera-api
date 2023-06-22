from models import Meal_Plan_Snack_Model
from .Base_Domain import Base_Domain
from dto.Meal_Plan_Snack_DTO import Meal_Plan_Snack_DTO
from uuid import UUID


class Meal_Plan_Snack_Domain(Base_Domain):
    def __init__(
        self, meal_plan_snack_object: Meal_Plan_Snack_Model | Meal_Plan_Snack_DTO
    ) -> None:
        self.id: UUID = meal_plan_snack_object.id
        self.snack_id: UUID = meal_plan_snack_object.snack_id
        self.meal_plan_id: UUID = meal_plan_snack_object.meal_plan_id
        self.multiplier: float = meal_plan_snack_object.multiplier
        self.active: bool = meal_plan_snack_object.active
