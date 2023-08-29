from repository.Base_Repository import Base_Repository
from models import Meal_Plan_Meal_Model
from uuid import UUID
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from domain.Meal_Plan_Meal_Domain import Meal_Plan_Meal_Domain
    from domain.Meal_Plan_Domain import Meal_Plan_Domain


class Meal_Plan_Meal_Repository(Base_Repository):
    def get_meal_plan_meal(
        self,
        meal_plan_meal_id: UUID = None,
        meal_id: UUID = None,
        meal_plan_id: UUID = None,
    ) -> Optional[Meal_Plan_Meal_Model]:
        if meal_plan_meal_id:
            meal_plan_meal: Optional[Meal_Plan_Meal_Model] = (
                self.db.session.query(Meal_Plan_Meal_Model)
                .filter(Meal_Plan_Meal_Model.id == meal_plan_meal_id)
                .first()
            )
        else:
            meal_plan_meal: Optional[Meal_Plan_Meal_Model] = (
                self.db.session.query(Meal_Plan_Meal_Model)
                .filter(
                    Meal_Plan_Meal_Model.meal_plan_id == meal_plan_id,
                    Meal_Plan_Meal_Model.meal_id == meal_id,
                )
                .first()
            )
        return meal_plan_meal

    def get_meal_plan_meals(
        self, meal_plan_id: UUID = None
    ) -> Optional[list[Meal_Plan_Meal_Model]]:
        meal_plan_meals_to_return: Optional[list[Meal_Plan_Meal_Model]] = []
        if meal_plan_id:
            try:
                meal_plan_meals_to_return = (
                    self.db.session.query(Meal_Plan_Meal_Model)
                    .filter(Meal_Plan_Meal_Model.meal_plan_id == meal_plan_id)
                    .all()
                )
            except:
                meal_plan_meals_to_return = None
        else:
            try:
                meal_plan_meals_to_return = self.db.session.query(
                    Meal_Plan_Meal_Model
                ).all()
            except:
                meal_plan_meals_to_return = None
        return meal_plan_meals_to_return

    def create_meal_plan_meal(
        self, meal_plan_meal_domain: "Meal_Plan_Meal_Domain"
    ) -> None:
        meal_plan_meal_to_create: Meal_Plan_Meal_Model = Meal_Plan_Meal_Model(
            meal_plan_meal_domain=meal_plan_meal_domain
        )
        self.db.session.add(meal_plan_meal_to_create)
        self.db.session.commit()
        return

    def update_meal_plan_meal(
        self,
        meal_plan_meal_domain: "Meal_Plan_Meal_Domain",
    ) -> None:
        odd_meal_plan_meal: Meal_Plan_Meal_Model = (
            self.db.session.query(Meal_Plan_Meal_Model)
            .filter(Meal_Plan_Meal_Model.id == meal_plan_meal_domain.id)
            .first()
        )
        odd_meal_plan_meal.update_multiplier(meal_plan_meal=meal_plan_meal_domain)
        # Odd and even meal plans have identical values for meal calories (but snacks will differ), so we can just copy the odd values to the even values
        self.db.session.commit()
        return

    def initialize_meal_plan_meals(self) -> None:
        from pathlib import Path
        from utils.load_json import load_json
        from domain.Meal_Plan_Meal_Domain import Meal_Plan_Meal_Domain
        from dto.Meal_Plan_Meal_DTO import Meal_Plan_Meal_DTO

        meal_plan_meal_json_file = Path(
            ".", "nutrient_data", "new_meal_plan_meals.json"
        )
        meal_plan_meals_data = load_json(filename=meal_plan_meal_json_file)

        # Only initialize custom values, not USDA values which are initialized alongside Meal_Plan_Models
        for meal_plan_json in meal_plan_meals_data:
            meal_plan_meal_dto = Meal_Plan_Meal_DTO(meal_plan_meal_json=meal_plan_json)
            meal_plan_meal_domain = Meal_Plan_Meal_Domain(
                meal_plan_meal_object=meal_plan_meal_dto
            )
            meal_plan_meal_model = Meal_Plan_Meal_Model(
                meal_plan_meal_domain=meal_plan_meal_domain
            )
            self.db.session.add(meal_plan_meal_model)
        self.db.session.commit()
