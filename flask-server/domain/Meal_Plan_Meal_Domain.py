from models import Meal_Plan_Meal_Model
from .Base_Domain import Base_Domain
from dto.Meal_Plan_Meal_DTO import Meal_Plan_Meal_DTO
from uuid import UUID


class Meal_Plan_Meal_Domain(Base_Domain):
    def __init__(
        self, meal_plan_meal_object: Meal_Plan_Meal_Model | Meal_Plan_Meal_DTO
    ) -> None:
        self.id: UUID = meal_plan_meal_object.id
        self.meal_id: UUID = meal_plan_meal_object.meal_id
        self.meal_plan_id: UUID = meal_plan_meal_object.meal_plan_id
        self.multiplier: float = meal_plan_meal_object.multiplier
        self.active: bool = meal_plan_meal_object.active
