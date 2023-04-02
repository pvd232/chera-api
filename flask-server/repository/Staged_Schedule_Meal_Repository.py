from repository.Base_Repository import Base_Repository
from models import Staged_Schedule_Meal_Model
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from domain.Staged_Schedule_Meal_Domain import Staged_Schedule_Meal_Domain


class Staged_Schedule_Meal_Repository(Base_Repository):
    def create_staged_schedule_meals(self,  staged_schedule_meal_domains: list['Staged_Schedule_Meal_Domain']) -> None:
        for staged_schedule_meal_domain in staged_schedule_meal_domains:
            new_staged_schedule_meal = Staged_Schedule_Meal_Model(
                staged_schedule_meal_domain=staged_schedule_meal_domain)
            self.db.session.add(new_staged_schedule_meal)
        self.db.session.commit()
        return

    def get_staged_schedule_meals(self,  staged_client_id: str) -> Optional[list[Staged_Schedule_Meal_Model]]:
        staged_schedule_meals = self.db.session.query(Staged_Schedule_Meal_Model).filter(
            Staged_Schedule_Meal_Model.staged_client_id == staged_client_id).all()
        return staged_schedule_meals
