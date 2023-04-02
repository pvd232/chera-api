from .USDA_Ingredient_Domain import USDA_Ingredient_Domain
from .USDA_Ingredient_Portion_Domain import USDA_Ingredient_Portion_Domain
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models import USDA_Ingredient_Model


class Extended_USDA_Ingredient_Domain(USDA_Ingredient_Domain):
    def __init__(self, usda_ingredient_model: 'USDA_Ingredient_Model') -> None:
        super().__init__(usda_ingredient_object=usda_ingredient_model)
        self.portions = [USDA_Ingredient_Portion_Domain(
            usda_ingredient_portion_object=x) for x in usda_ingredient_model.portions]
