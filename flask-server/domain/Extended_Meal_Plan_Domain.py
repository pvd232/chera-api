from .Meal_Plan_Domain import Meal_Plan_Domain
from .USDA_Nutrient_Daily_Value_Domain import USDA_Nutrient_Daily_Value_Domain
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models import Meal_Plan_Model


class Extended_Meal_Plan_Domain(Meal_Plan_Domain):
    def __init__(self, meal_plan_model: 'Meal_Plan_Model') -> None:
        super().__init__(meal_plan_object=meal_plan_model)
        self.usda_nutrient_daily_values = [USDA_Nutrient_Daily_Value_Domain(
            usda_nutrient_daily_value_object=x) for x in meal_plan_model.usda_nutrient_daily_values]
