from .Base_Domain import Base_Domain
from uuid import UUID

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .Extended_Recipe_Ingredient_Nutrient_Domain import Extended_Recipe_Ingredient_Nutrient_Domain


class Compressed_Nutrient_Data_Domain(Base_Domain):
    def __init__(self, extended_recipe_ingredient_nutrient_Domain: 'Extended_Recipe_Ingredient_Nutrient_Domain') -> None:
        self.id: UUID = extended_recipe_ingredient_nutrient_Domain.id
        self.recipe_ingredient_id: UUID = extended_recipe_ingredient_nutrient_Domain.recipe_ingredient_id
        self.nutrient_id: str = extended_recipe_ingredient_nutrient_Domain.nutrient_id
        self.usda_nutrient_daily_value_amount: float = extended_recipe_ingredient_nutrient_Domain.usda_nutrient_daily_value_amount
        self.amount: float = extended_recipe_ingredient_nutrient_Domain.amount
