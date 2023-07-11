from models import Meal_Plan_Model
from repository.Base_Repository import Base_Repository
import uuid
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from domain.Meal_Plan_Domain import Meal_Plan_Domain


class Meal_Plan_Repository(Base_Repository):
    def get_meal_plan(
        self, meal_plan_id: uuid.UUID = None, meal_plan_number: int = None
    ) -> Meal_Plan_Model:
        if meal_plan_id and not meal_plan_number:
            meal_plan = (
                self.db.session.query(Meal_Plan_Model)
                .filter(Meal_Plan_Model.id == meal_plan_id)
                .first()
            )
            return meal_plan
        else:
            meal_plan = (
                self.db.session.query(Meal_Plan_Model)
                .filter(Meal_Plan_Model.number == meal_plan_number)
                .first()
            )
            return meal_plan

    def get_even_meal_plan(self, odd_meal_plan_id: uuid.UUID) -> Meal_Plan_Model:
        odd_meal_plan = self.get_meal_plan(meal_plan_id=odd_meal_plan_id)
        even_meal_plan = (
            self.db.session.query(Meal_Plan_Model)
            .filter(Meal_Plan_Model.number == odd_meal_plan.number + 1)
            .first()
        )
        return even_meal_plan

    def get_meal_plans(self) -> list[Meal_Plan_Model]:
        meal_plans = self.db.session.query(Meal_Plan_Model).all()
        return meal_plans

    def get_odd_meal_plans(self) -> list[Meal_Plan_Model]:
        meal_plans = (
            self.db.session.query(Meal_Plan_Model)
            .filter(Meal_Plan_Model.number % 2 == 1)
            .all()
        )
        return meal_plans

    def initialize_meal_plans(self) -> None:
        from pathlib import Path
        from utils.load_json import load_json
        from domain.Meal_Plan_Domain import Meal_Plan_Domain
        from dto.Meal_Plan_DTO import Meal_Plan_DTO

        meal_plan_json_file = Path(".", "nutrient_data", "new_meal_plans.json")
        meal_plans_data = load_json(filename=meal_plan_json_file)

        for meal_plan_json in meal_plans_data:
            meal_plan_dto = Meal_Plan_DTO(meal_plan_json=meal_plan_json)
            meal_plan_domain = Meal_Plan_Domain(meal_plan_object=meal_plan_dto)

            meal_plan_model = Meal_Plan_Model(meal_plan_domain=meal_plan_domain)
            self.db.session.add(meal_plan_model)
        self.db.session.commit()
