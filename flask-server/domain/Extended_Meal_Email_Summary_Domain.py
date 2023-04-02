from .Meal_Domain import Meal_Domain
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models import Meal_Model


class Extended_Meal_Email_Summary_Domain(Meal_Domain):
    def __init__(self, meal_model: 'Meal_Model') -> None:
        super().__init__(meal_object=meal_model)
        self.quantity = 1

    def __str__(self) -> str:
        return '<p style= "font-weight:bold; font-size: medium;">Meals In Order:</p> <p style="font-size:medium;">{0}</p> <p style="font-size:medium;">{1}</p><br>'.format(str(self.quantity) + 'x ' + self.name, self.description)
