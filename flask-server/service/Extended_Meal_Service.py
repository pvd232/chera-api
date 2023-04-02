from .Meal_Service import Meal_Service
from domain.Extended_Meal_Domain import Extended_Meal_Domain
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from models import Meal_Model


class Extended_Meal_Service(Meal_Service):
    def get_extended_meals(self) -> Optional[list['Extended_Meal_Domain']]:
        meals: Optional[list['Meal_Model']] = self.meal_repository.get_meals()
        if meals:
            return [Extended_Meal_Domain(meal_model=x) for x in meals]
        else:
            return None
