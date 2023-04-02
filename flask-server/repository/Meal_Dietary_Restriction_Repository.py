from .Base_Repository import Base_Repository
from models import Meal_Dietary_Restriction_Model
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from domain.Meal_Dietary_Restriction_Domain import Meal_Dietary_Restriction_Domain


class Meal_Dietary_Restriction_Repository(Base_Repository):
    def create_meal_dietary_restriction(self, meal_dietary_restriction_domain: 'Meal_Dietary_Restriction_Domain') -> None:
        new_meal_dietary_restriction = Meal_Dietary_Restriction_Model(
            meal_dietary_restriction_domain=meal_dietary_restriction_domain)
        self.db.session.add(new_meal_dietary_restriction)
        self.db.session.commit()
        return
