from .Recipe_Ingredient_Nutrient_Domain import Recipe_Ingredient_Nutrient_Domain
from .Nutrient_Domain import Nutrient_Domain
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models import Recipe_Ingredient_Nutrient_Model


class Extended_Recipe_Ingredient_Nutrient_Domain(Recipe_Ingredient_Nutrient_Domain):
    def __init__(self, recipe_ingredient_nutrient_model: 'Recipe_Ingredient_Nutrient_Model') -> None:
        super().__init__(recipe_ingredient_nutrient_object=recipe_ingredient_nutrient_model)
        self.nutrient_name = recipe_ingredient_nutrient_model.nutrient.name
        self.nutrient_unit = recipe_ingredient_nutrient_model.nutrient.unit
        self.usda_nutrient_id = recipe_ingredient_nutrient_model.nutrient.usda_id
