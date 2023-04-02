from .Meal_Domain import Meal_Domain
from .Meal_Dietary_Restriction_Domain import Meal_Dietary_Restriction_Domain
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models import Meal_Model


class Extended_Meal_Domain(Meal_Domain):
    def __init__(self, meal_model: 'Meal_Model') -> None:
        super().__init__(meal_object=meal_model)
        self.dietary_restrictions = [Meal_Dietary_Restriction_Domain(
            meal_dietary_restriction_object=x) for x in meal_model.dietary_restrictions]
