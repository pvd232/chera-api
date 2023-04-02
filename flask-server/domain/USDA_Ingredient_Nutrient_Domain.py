from .Base_Domain import Base_Domain
from typing import TYPE_CHECKING
from models import USDA_Ingredient_Nutrient_Model
from dto.USDA_Ingredient_Nutrient_DTO import USDA_Ingredient_Nutrient_DTO


class USDA_Ingredient_Nutrient_Domain(Base_Domain):
    def __init__(self, usda_ingredient_nutrient_object: USDA_Ingredient_Nutrient_Model | USDA_Ingredient_Nutrient_DTO) -> None:
        self.id = usda_ingredient_nutrient_object.id
        self.usda_ingredient_id = usda_ingredient_nutrient_object.usda_ingredient_id
        self.nutrient_id = usda_ingredient_nutrient_object.nutrient_id
        self.amount = usda_ingredient_nutrient_object.amount
