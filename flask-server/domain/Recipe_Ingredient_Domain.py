from models import Recipe_Ingredient_Model
from .Base_Domain import Base_Domain
from dto.Recipe_Ingredient_DTO import Recipe_Ingredient_DTO


class Recipe_Ingredient_Domain(Base_Domain):
    def __init__(self, recipe_ingredient_object: Recipe_Ingredient_Model | Recipe_Ingredient_DTO) -> None:
        self.id = recipe_ingredient_object.id
        self.usda_ingredient_id = recipe_ingredient_object.usda_ingredient_id
        self.meal_plan_meal_id = recipe_ingredient_object.meal_plan_meal_id
        self.usda_ingredient_portion_id = recipe_ingredient_object.usda_ingredient_portion_id
        self.quantity = recipe_ingredient_object.quantity
        self.active = recipe_ingredient_object.active
