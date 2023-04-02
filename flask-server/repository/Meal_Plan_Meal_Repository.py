from repository.Base_Repository import Base_Repository
from models import Meal_Plan_Meal_Model
from uuid import UUID
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from domain.Meal_Plan_Meal_Domain import Meal_Plan_Meal_Domain


class Meal_Plan_Meal_Repository(Base_Repository):
    def get_meal_plan_meal(self,  meal_plan_meal_id: UUID) -> Optional[Meal_Plan_Meal_Model]:
        meal_plan_meal: Optional[Meal_Plan_Meal_Model] = self.db.session.query(Meal_Plan_Meal_Model).filter(
            Meal_Plan_Meal_Model.id == meal_plan_meal_id).first()
        return meal_plan_meal

    def get_meal_plan_meals(self,  meal_plan_id: UUID = None) -> Optional[list[Meal_Plan_Meal_Model]]:
        if not meal_plan_id:
            meal_plan_meals: Optional[list[Meal_Plan_Meal_Model]] = self.db.session.query(
                Meal_Plan_Meal_Model).all()
            return meal_plan_meals
        else:
            meal_plan_meals: Optional[list[Meal_Plan_Meal_Model]] = self.db.session.query(Meal_Plan_Meal_Model).filter(
                Meal_Plan_Meal_Model.meal_plan_id == meal_plan_id).all()
            if meal_plan_meals:
                return meal_plan_meals
            else:
                return None

    def create_meal_plan_meal(self,  meal_plan_meal_domain: 'Meal_Plan_Meal_Domain') -> None:
        meal_plan_meal_to_create: Meal_Plan_Meal_Model = Meal_Plan_Meal_Model(
            meal_plan_meal_domain=meal_plan_meal_domain)
        self.db.session.add(meal_plan_meal_to_create)
        self.db.session.commit()
        return

    def update_meal_plan_meal(self,  odd_meal_plan_meal: 'Meal_Plan_Meal_Domain', even_meal_plan_meal: 'Meal_Plan_Meal_Domain') -> None:
        odd_meal_plan_meal_to_update: Optional[Meal_Plan_Meal_Model] = self.db.session.query(
            Meal_Plan_Meal_Model).filter(Meal_Plan_Meal_Model.id == odd_meal_plan_meal.id).first()
        if odd_meal_plan_meal_to_update:
            odd_meal_plan_meal_to_update.update(
                meal_plan_meal=odd_meal_plan_meal)

        even_meal_plan_meal_to_update = self.db.session.query(
            Meal_Plan_Meal_Model).filter(Meal_Plan_Meal_Model.id == even_meal_plan_meal.id).first()
        if even_meal_plan_meal_to_update:
            # even meal plan meals will have the same number of calories for meals, only snacks differ, so the odd meal plan values will be cloned
            even_meal_plan_meal_to_update.update(odd_meal_plan_meal)
        self.db.session.commit()
        return
