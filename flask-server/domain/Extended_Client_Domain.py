from .Client_Domain import Client_Domain
from .Meal_Plan_Domain import Meal_Plan_Domain
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models import Client_Model


class Extended_Client_Domain(Client_Domain):
    def __init__(self, client_model: 'Client_Model') -> None:
        super().__init__(client_object=client_model)
        self.meal_plan = Meal_Plan_Domain(
            meal_plan_object=client_model.meal_plan)
