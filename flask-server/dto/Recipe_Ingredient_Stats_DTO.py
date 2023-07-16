from .Base_DTO import Base_DTO
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .Extended_Recipe_Ingredient_DTO import Extended_Recipe_Ingredient_DTO


class Recipe_Ingredient_Stats_DTO:
    def __init__(self, extended_recipe_ingredient_dto: Extended_Recipe_Ingredient_DTO):
        self.usda_ingredient_name = extended_recipe_ingredient_dto.usda_ingredient_name
        self.amount_of_grams = extended_recipe_ingredient_dto.amount_of_grams
