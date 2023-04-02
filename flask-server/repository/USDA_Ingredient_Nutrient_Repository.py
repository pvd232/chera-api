from repository.Base_Repository import Base_Repository
from models import USDA_Ingredient_Nutrient_Model
from typing import Optional


class USDA_Ingredient_Nutrient_Repository(Base_Repository):
    def get_usda_ingredient_nutrients(self, usda_ingredient_id: str) -> list[USDA_Ingredient_Nutrient_Model]:
        usda_ingredient_nutrients = self.db.session.query(
            USDA_Ingredient_Nutrient_Model).filter(USDA_Ingredient_Nutrient_Model.usda_ingredient_id == usda_ingredient_id).all()
        return usda_ingredient_nutrients
