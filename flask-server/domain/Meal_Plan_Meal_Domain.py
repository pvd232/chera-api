from models import Meal_Plan_Meal_Model
from .Base_Domain import Base_Domain
from dto.Meal_Plan_Meal_DTO import Meal_Plan_Meal_DTO


class Meal_Plan_Meal_Domain(Base_Domain):
    def __init__(self, meal_plan_meal_object: Meal_Plan_Meal_Model | Meal_Plan_Meal_DTO) -> None:
        self.id = meal_plan_meal_object.id
        self.meal_id = meal_plan_meal_object.meal_id
        self.meal_plan_id = meal_plan_meal_object.meal_plan_id
        self.active = meal_plan_meal_object.active
