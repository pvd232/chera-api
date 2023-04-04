from repository.Base_Repository import Base_Repository
from models import USDA_Ingredient_Nutrient_Model
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from domain.USDA_Ingredient_Nutrient_Domain import USDA_Ingredient_Nutrient_Domain


class USDA_Ingredient_Nutrient_Repository(Base_Repository):
    def get_usda_ingredient_nutrients(self, usda_ingredient_id: str) -> list[USDA_Ingredient_Nutrient_Model]:
        usda_ingredient_nutrients = self.db.session.query(
            USDA_Ingredient_Nutrient_Model).filter(USDA_Ingredient_Nutrient_Model.usda_ingredient_id == usda_ingredient_id).all()
        return usda_ingredient_nutrients

    def create_usda_ingredient_nutrients(self, usda_ingredient_nutrient_domains: list['USDA_Ingredient_Nutrient_Domain']) -> None:
        for usda_ingredient_nutrient_domain in usda_ingredient_nutrient_domains:
            new_usda_ingredient_nutrient = USDA_Ingredient_Nutrient_Model(
                usda_ingredient_nutrient_domain=usda_ingredient_nutrient_domain)
            self.db.session.add(new_usda_ingredient_nutrient)
        self.db.session.commit()
