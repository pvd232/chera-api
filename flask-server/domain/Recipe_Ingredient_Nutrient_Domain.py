from models import Recipe_Ingredient_Nutrient_Model
from .Base_Domain import Base_Domain
from dto.Recipe_Ingredient_Nutrient_DTO import Recipe_Ingredient_Nutrient_DTO
from uuid import UUID


class Recipe_Ingredient_Nutrient_Domain(Base_Domain):
    def __init__(self, recipe_ingredient_nutrient_object: Recipe_Ingredient_Nutrient_Model | Recipe_Ingredient_Nutrient_DTO) -> None:
        if recipe_ingredient_nutrient_object:
            self.id: UUID = recipe_ingredient_nutrient_object.id
            self.recipe_ingredient_id: UUID = recipe_ingredient_nutrient_object.recipe_ingredient_id
            self.nutrient_id: str = recipe_ingredient_nutrient_object.nutrient_id
            self.amount: float = recipe_ingredient_nutrient_object.amount
            self.usda_nutrient_daily_value_amount: float = recipe_ingredient_nutrient_object.usda_nutrient_daily_value_amount
