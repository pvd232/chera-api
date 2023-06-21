from repository.Base_Repository import Base_Repository
from models import Meal_Plan_Snack_Model
from uuid import UUID
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from domain.Meal_Plan_Snack_Domain import Meal_Plan_Snack_Domain


class Meal_Plan_Snack_Repository(Base_Repository):
    def get_meal_plan_snack(
        self, meal_plan_snack_id: UUID
    ) -> Optional[Meal_Plan_Snack_Model]:
        meal_plan_snack: Optional[Meal_Plan_Snack_Model] = (
            self.db.session.query(Meal_Plan_Snack_Model)
            .filter(Meal_Plan_Snack_Model.id == meal_plan_snack_id)
            .first()
        )
        return meal_plan_snack

    def get_meal_plan_snacks(
        self, meal_plan_id: UUID = None
    ) -> Optional[list[Meal_Plan_Snack_Model]]:
        if not meal_plan_id:
            meal_plan_snacks: Optional[
                list[Meal_Plan_Snack_Model]
            ] = self.db.session.query(Meal_Plan_Snack_Model).all()
            return meal_plan_snacks
        else:
            meal_plan_snacks: Optional[list[Meal_Plan_Snack_Model]] = (
                self.db.session.query(Meal_Plan_Snack_Model)
                .filter(Meal_Plan_Snack_Model.meal_plan_id == meal_plan_id)
                .all()
            )
            if meal_plan_snacks:
                return meal_plan_snacks
            else:
                return None

    def create_meal_plan_snack(
        self, meal_plan_snack_domain: "Meal_Plan_Snack_Domain"
    ) -> None:
        meal_plan_snack_to_create: Meal_Plan_Snack_Model = Meal_Plan_Snack_Model(
            meal_plan_snack_domain=meal_plan_snack_domain
        )
        self.db.session.add(meal_plan_snack_to_create)
        self.db.session.commit()
        return

    def update_meal_plan_snack(
        self,
        odd_meal_plan_snack: "Meal_Plan_Snack_Domain",
        even_meal_plan_snack: "Meal_Plan_Snack_Domain",
    ) -> None:
        odd_meal_plan_snack_to_update: Optional[Meal_Plan_Snack_Model] = (
            self.db.session.query(Meal_Plan_Snack_Model)
            .filter(Meal_Plan_Snack_Model.id == odd_meal_plan_snack.id)
            .first()
        )
        if odd_meal_plan_snack_to_update:
            odd_meal_plan_snack_to_update.update(meal_plan_snack=odd_meal_plan_snack)

        even_meal_plan_snack_to_update = (
            self.db.session.query(Meal_Plan_Snack_Model)
            .filter(Meal_Plan_Snack_Model.id == even_meal_plan_snack.id)
            .first()
        )
        if even_meal_plan_snack_to_update:
            # even meal plan meals will have the same number of calories for meals, only snacks differ, so the odd meal plan values will be cloned
            even_meal_plan_snack_to_update.update(odd_meal_plan_snack)
        self.db.session.commit()
        return

    def initialize_meal_plan_snacks(self) -> None:
        from pathlib import Path
        from utils.load_json import load_json
        from domain.Meal_Plan_Snack_Domain import Meal_Plan_Snack_Domain
        from dto.Meal_Plan_Snack_DTO import Meal_Plan_Snack_DTO

        meal_plan_snack_json_file = Path(
            ".", "nutrient_data", "new_meal_plan_snacks.json"
        )
        meal_plan_snacks_data = load_json(filename=meal_plan_snack_json_file)

        # Only initialize custom values, not USDA values which are initialized alongside Meal_Plan_Models
        for meal_plan_json in meal_plan_snacks_data:
            meal_plan_snack_dto = Meal_Plan_Snack_DTO(
                meal_plan_snack_json=meal_plan_json
            )
            meal_plan_snack_domain = Meal_Plan_Snack_Domain(
                meal_plan_snack_object=meal_plan_snack_dto
            )
            meal_plan_snack_model = Meal_Plan_Snack_Model(
                meal_plan_snack_domain=meal_plan_snack_domain
            )
            self.db.session.add(meal_plan_snack_model)
        self.db.session.commit()
