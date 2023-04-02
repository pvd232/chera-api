from .Recipe_Ingredient_Nutrient_DTO import Recipe_Ingredient_Nutrient_DTO
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from domain.Extended_Recipe_Ingredient_Nutrient_Domain import Extended_Recipe_Ingredient_Nutrient_Domain


class Extended_Recipe_Ingredient_Nutrient_DTO(Recipe_Ingredient_Nutrient_DTO):
    def __init__(self, extended_recipe_ingredient_nutrient_domain: 'Extended_Recipe_Ingredient_Nutrient_Domain') -> None:
        super().__init__(recipe_ingredient_nutrient_domain=extended_recipe_ingredient_nutrient_domain)
        self.nutrient_name = extended_recipe_ingredient_nutrient_domain.nutrient_name
        self.nutrient_unit = extended_recipe_ingredient_nutrient_domain.nutrient_unit
        self.usda_nutrient_id = extended_recipe_ingredient_nutrient_domain.usda_nutrient_id
