from repository.Base_Repository import Base_Repository
from models import USDA_Ingredient_Model
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from domain.Recipe_Ingredient_Domain import Recipe_Ingredient_Domain


class USDA_Ingredient_Repository(Base_Repository):
    def get_usda_ingredients(self) -> list[USDA_Ingredient_Model]:
        usda_ingredients = self.db.session.query(USDA_Ingredient_Model).all()
        return usda_ingredients

    def get_usda_ingredient(self, usda_ingredient_id: str) -> USDA_Ingredient_Model | None:
        usda_ingredient = self.db.session.query(USDA_Ingredient_Model).filter(
            USDA_Ingredient_Model.id == usda_ingredient_id).first()
        return usda_ingredient

    def update_usda_ingredient(self, usda_ingredient_id: str, recipe_ingredient_domain: 'Recipe_Ingredient_Domain') -> None:
        usda_ingredient_to_update: USDA_Ingredient_Model = self.db.session.query(USDA_Ingredient_Model).filter(
            USDA_Ingredient_Model.id == usda_ingredient_id).first()
        usda_ingredient_to_update.update(
            updated_recipe_ingredient=recipe_ingredient_domain)
        self.db.session.commit()
