from repository.Base_Repository import Base_Repository
from models import USDA_Nutrient_Daily_Value_Model
from uuid import UUID


class USDA_Nutrient_Daily_Value_Repository(Base_Repository):
    def get_usda_nutrient_daily_value(self, meal_plan_id: UUID, nutrient_id: str) -> USDA_Nutrient_Daily_Value_Model:
        usda_nutrient_daily_value = self.db.session.query(
            USDA_Nutrient_Daily_Value_Model).filter(USDA_Nutrient_Daily_Value_Model.meal_plan_id == meal_plan_id, USDA_Nutrient_Daily_Value_Model.nutrient_id == nutrient_id).first()
        return usda_nutrient_daily_value
