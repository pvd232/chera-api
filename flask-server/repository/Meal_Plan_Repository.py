from models import Meal_Plan_Model
from repository.Base_Repository import Base_Repository
import uuid
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from domain.Meal_Plan_Domain import Meal_Plan_Domain


class Meal_Plan_Repository(Base_Repository):
    def get_meal_plan(self,  meal_plan_id: uuid.UUID) -> Meal_Plan_Model:
        meal_plan = self.db.session.query(Meal_Plan_Model).filter(Meal_Plan_Model.id == meal_plan_id).first(
        )
        return meal_plan

    def get_meal_plans(self) -> list[Meal_Plan_Model]:
        meal_plans = self.db.session.query(Meal_Plan_Model).all()
        return meal_plans

    def update_meal_plans(self,  new_meal_plans: list['Meal_Plan_Domain']) -> None:
        current_meal_plans: list[Meal_Plan_Model] = self.db.session.query(
            Meal_Plan_Model).all()
        for updated_meal_plan in new_meal_plans:
            meal_plan_was_updated = False
            for meal_plan in current_meal_plans:
                if meal_plan.number == updated_meal_plan.number:
                    meal_plan.stated_caloric_lower_bound = updated_meal_plan.stated_caloric_lower_bound
                    meal_plan.stated_caloric_upper_bound = updated_meal_plan.stated_caloric_upper_bound
                    meal_plan.breakfast_calories = updated_meal_plan.breakfast_calories
                    meal_plan.lunch_calories = updated_meal_plan.lunch_calories
                    meal_plan.dinner_calories = updated_meal_plan.dinner_calories
                    meal_plan.number_of_snacks = updated_meal_plan.number_of_snacks
                    meal_plan.per_snack_caloric_lower_bound = updated_meal_plan.per_snack_caloric_lower_bound
                    meal_plan.per_snack_caloric_upper_bound = updated_meal_plan.per_snack_caloric_upper_bound
                    meal_plan_was_updated = True
                    break
            if not meal_plan_was_updated:
                updated_meal_plan.id = uuid.uuid4()
                new_meal_plan = Meal_Plan_Model(
                    meal_plan_domain=updated_meal_plan)
                self.db.session.add(new_meal_plan)
        self.db.session.commit()
