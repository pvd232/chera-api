from .USDA_Ingredient_Service import USDA_Ingredient_Service
from domain.Extended_USDA_Ingredient_Domain import Extended_USDA_Ingredient_Domain
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from models import USDA_Ingredient_Model


class Extended_USDA_Ingredient_Service(USDA_Ingredient_Service):
    def get_extended_usda_ingredients(self) -> Optional[list['Extended_USDA_Ingredient_Domain']]:
        usda_ingredients: Optional[list['USDA_Ingredient_Model']
                                   ] = self.usda_ingredient_repository.get_usda_ingredients()
        if usda_ingredients:
            return [Extended_USDA_Ingredient_Domain(usda_ingredient_model=x) for x in usda_ingredients]
        else:
            return None
