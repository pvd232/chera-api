from uuid import UUID
from typing import TYPE_CHECKING
from .Base_DTO import Base_DTO
if TYPE_CHECKING:
    from domain.Recipe_Ingredient_Nutrient_Domain import Recipe_Ingredient_Nutrient_Domain


class Recipe_Ingredient_Nutrient_DTO(Base_DTO):
    def __init__(self, recipe_ingredient_nutrient_json: dict = None, recipe_ingredient_nutrient_domain: 'Recipe_Ingredient_Nutrient_Domain' = None) -> None:
        # UUID attributes will always be UUIDs as they are created in the backend (see MenuBuilder related stack)
        if recipe_ingredient_nutrient_json:
            self.id: UUID = recipe_ingredient_nutrient_json["id"]
            self.recipe_ingredient_id: UUID = recipe_ingredient_nutrient_json[
                "recipe_ingredient_id"]
            self.nutrient_id: str = recipe_ingredient_nutrient_json["nutrient_id"]
            self.usda_nutrient_daily_value_amount: float = float(recipe_ingredient_nutrient_json[
                "usda_nutrient_daily_value_amount"])
            self.amount: float = recipe_ingredient_nutrient_json["amount"]

        elif recipe_ingredient_nutrient_domain:
            self.id: UUID = recipe_ingredient_nutrient_domain.id
            self.recipe_ingredient_id: UUID = recipe_ingredient_nutrient_domain.recipe_ingredient_id
            self.nutrient_id: str = recipe_ingredient_nutrient_domain.nutrient_id
            self.usda_nutrient_daily_value_amount: float = recipe_ingredient_nutrient_domain.usda_nutrient_daily_value_amount
            self.amount: float = recipe_ingredient_nutrient_domain.amount
