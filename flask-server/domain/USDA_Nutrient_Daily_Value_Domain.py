from models import USDA_Nutrient_Daily_Value_Model
from .Base_Domain import Base_Domain


class USDA_Nutrient_Daily_Value_Domain(Base_Domain):
    def __init__(self, usda_nutrient_daily_value_object: USDA_Nutrient_Daily_Value_Model) -> None:
        self.id = usda_nutrient_daily_value_object.id
        self.nutrient_id = usda_nutrient_daily_value_object.nutrient_id
        self.meal_plan_id = usda_nutrient_daily_value_object.meal_plan_id
        self.amount = usda_nutrient_daily_value_object.amount
        self.unit = usda_nutrient_daily_value_object.unit
