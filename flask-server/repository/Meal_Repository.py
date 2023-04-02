from repository.Base_Repository import Base_Repository
from models import Meal_Model
from uuid import UUID
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from domain.Meal_Domain import Meal_Domain


class Meal_Repository(Base_Repository):
    def get_meal(self,  meal_id: UUID) -> Optional[Meal_Model]:
        meal = self.db.session.query(Meal_Model).filter(
            Meal_Model.id == meal_id).first()
        return meal

    def get_meals(self) -> Optional[list[Meal_Model]]:
        meals = self.db.session.query(Meal_Model).all()
        return meals

    def create_meal(self, meal_domain: 'Meal_Domain') -> None:
        new_meal_model = Meal_Model(
            meal_domain=meal_domain)
        self.db.session.add(new_meal_model)
        self.db.session.commit()
        return
