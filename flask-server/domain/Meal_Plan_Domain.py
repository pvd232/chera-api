from models import Meal_Plan_Model
from .Base_Domain import Base_Domain
from dto.Meal_Plan_DTO import Meal_Plan_DTO


class Meal_Plan_Domain(Base_Domain):
    def __init__(self, meal_plan_object: Meal_Plan_Model | Meal_Plan_DTO) -> None:
        self.id = meal_plan_object.id
        self.number = meal_plan_object.number
        self.breakfast_calories = meal_plan_object.breakfast_calories
        self.lunch_calories = meal_plan_object.lunch_calories
        self.dinner_calories = meal_plan_object.dinner_calories
        self.stated_caloric_lower_bound = meal_plan_object.stated_caloric_lower_bound
        self.stated_caloric_upper_bound = meal_plan_object.stated_caloric_upper_bound
        self.number_of_snacks = meal_plan_object.number_of_snacks
        self.per_snack_caloric_lower_bound = meal_plan_object.per_snack_caloric_lower_bound
        self.per_snack_caloric_upper_bound = meal_plan_object.per_snack_caloric_upper_bound
