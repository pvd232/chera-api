from models import Meal_Plan_Snack_Model
from .Base_Domain import Base_Domain
from dto.Meal_Plan_Snack_DTO import Meal_Plan_Snack_DTO


class Meal_Plan_Snack_Domain(Base_Domain):
    def __init__(
        self, meal_plan_snack_object: Meal_Plan_Snack_Model | Meal_Plan_Snack_DTO
    ) -> None:
        self.id = meal_plan_snack_object.id
        self.snack_id = meal_plan_snack_object.snack_id
        self.meal_plan_id = meal_plan_snack_object.meal_plan_id
        self.active = meal_plan_snack_object.active
