from repository.Base_Repository import Base_Repository
from models import Meal_Plan_Snack_Model
from uuid import UUID
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from domain.Meal_Plan_Snack_Domain import Meal_Plan_Snack_Domain


class Meal_Plan_Snack_Repository(Base_Repository):
    def get_meal_plan_snack(
        self,
        meal_plan_snack_id: Optional[UUID] = None,
        meal_plan_id: Optional[UUID] = None,
        snack_id: Optional[UUID] = None,
    ) -> Optional[Meal_Plan_Snack_Model]:
        if meal_plan_snack_id:
            return (
                self.db.session.query(Meal_Plan_Snack_Model)
                .filter(Meal_Plan_Snack_Model.id == meal_plan_snack_id)
                .first()
            )
        else:
            return (
                self.db.session.query(Meal_Plan_Snack_Model)
                .filter(
                    Meal_Plan_Snack_Model.meal_plan_id == meal_plan_id,
                    Meal_Plan_Snack_Model.snack_id == snack_id,
                )
                .first()
            )

    def get_meal_plan_snacks(
        self, meal_plan_id: Optional[UUID] = None
    ) -> Optional[list[Meal_Plan_Snack_Model]]:
        if not meal_plan_id:
            meal_plan_snacks: Optional[list[Meal_Plan_Snack_Model]] = (
                self.db.session.query(Meal_Plan_Snack_Model).all()
            )
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

    def get_standard_meal_plan_snacks(self) -> Optional[list[Meal_Plan_Snack_Model]]:
        meal_plan_snacks: Optional[list[Meal_Plan_Snack_Model]] = (
            self.db.session.query(Meal_Plan_Snack_Model)
            .filter(Meal_Plan_Snack_Model.associated_meal_plan.has(number=3))
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
        meal_plan_snack_domain: "Meal_Plan_Snack_Domain",
    ) -> None:
        meal_plan_snack_to_update = (
            self.db.session.query(Meal_Plan_Snack_Model)
            .filter(Meal_Plan_Snack_Model.id == meal_plan_snack_domain.id)
            .first()
        )

        meal_plan_snack_to_update.update_multiplier(
            meal_plan_snack=meal_plan_snack_domain
        )

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
