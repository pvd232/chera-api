from .Staged_Client_Domain import Staged_Client_Domain
from .Meal_Plan_Domain import Meal_Plan_Domain
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models import Staged_Client_Model


class Extended_Staged_Client_Domain(Staged_Client_Domain):
    def __init__(self, staged_client_model: 'Staged_Client_Model') -> None:
        super().__init__(staged_client_object=staged_client_model)
        self.meal_plan = Meal_Plan_Domain(
            meal_plan_object=staged_client_model.meal_plan)
