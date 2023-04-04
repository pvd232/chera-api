from repository.Base_Repository import Base_Repository
from models import USDA_Ingredient_Portion_Model
from uuid import UUID
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from domain.Recipe_Ingredient_Domain import Recipe_Ingredient_Domain
    from domain.USDA_Ingredient_Portion_Domain import USDA_Ingredient_Portion_Domain


class USDA_Ingredient_Portion_Repository(Base_Repository):
    def get_usda_ingredient_portion(self, usda_ingredient_portion_id: UUID) -> USDA_Ingredient_Portion_Model:
        usda_ingredient_portion = self.db.session.query(USDA_Ingredient_Portion_Model).filter(
            USDA_Ingredient_Portion_Model.id == usda_ingredient_portion_id).first()
        return usda_ingredient_portion

    def get_recipe_ingredient_portions(self, recipe_ingredient_domain: 'Recipe_Ingredient_Domain') -> Optional[list[USDA_Ingredient_Portion_Model]]:
        usda_ingredient_portions = self.db.session.query(USDA_Ingredient_Portion_Model).filter(
            USDA_Ingredient_Portion_Model.usda_ingredient_id == recipe_ingredient_domain.usda_ingredient_id).all()
        return usda_ingredient_portions

    def create_usda_ingredient_portion(self, usda_ingredient_portion_domain: 'USDA_Ingredient_Portion_Domain') -> None:
        new_usda_ingredient_portion = USDA_Ingredient_Portion_Model(
            usda_ingredient_portion_domain=usda_ingredient_portion_domain)
        self.db.session.add(new_usda_ingredient_portion)
        self.db.session.commit()
