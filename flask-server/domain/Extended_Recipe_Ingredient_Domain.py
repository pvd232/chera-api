from domain.Recipe_Ingredient_Domain import Recipe_Ingredient_Domain
from domain.Extended_Recipe_Ingredient_Nutrient_Domain import Extended_Recipe_Ingredient_Nutrient_Domain
from domain.USDA_Ingredient_Domain import USDA_Ingredient_Domain
from domain.USDA_Ingredient_Portion_Domain import USDA_Ingredient_Portion_Domain
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models import Recipe_Ingredient_Model


class Extended_Recipe_Ingredient_Domain(Recipe_Ingredient_Domain):
    def __init__(self, recipe_ingredient_model: 'Recipe_Ingredient_Model') -> None:
        super().__init__(recipe_ingredient_object=recipe_ingredient_model)
        self.nutrients: list[Extended_Recipe_Ingredient_Nutrient_Domain] = [Extended_Recipe_Ingredient_Nutrient_Domain(
            recipe_ingredient_nutrient_model=x)for x in recipe_ingredient_model.nutrients]
        self.usda_ingredient = USDA_Ingredient_Domain(
            usda_ingredient_object=recipe_ingredient_model.usda_ingredient)
        self.usda_ingredient_portion = USDA_Ingredient_Portion_Domain(
            usda_ingredient_portion_object=recipe_ingredient_model.usda_ingredient_portion)
