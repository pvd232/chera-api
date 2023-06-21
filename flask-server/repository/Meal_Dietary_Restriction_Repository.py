from .Base_Repository import Base_Repository
from models import Meal_Dietary_Restriction_Model
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from domain.Meal_Dietary_Restriction_Domain import Meal_Dietary_Restriction_Domain


class Meal_Dietary_Restriction_Repository(Base_Repository):
    def get_meal_dietary_restrictions(self) -> list[Meal_Dietary_Restriction_Model]:
        meal_dietary_restrictions = self.db.session.query(
            Meal_Dietary_Restriction_Model
        ).all()
        return meal_dietary_restrictions

    def create_meal_dietary_restriction(
        self, meal_dietary_restriction_domain: "Meal_Dietary_Restriction_Domain"
    ) -> None:
        new_meal_dietary_restriction = Meal_Dietary_Restriction_Model(
            meal_dietary_restriction_domain=meal_dietary_restriction_domain
        )
        self.db.session.add(new_meal_dietary_restriction)
        self.db.session.commit()

    def initialize_meal_dietary_restrictions(self) -> None:
        from pathlib import Path
        from utils.load_json import load_json
        from domain.Meal_Dietary_Restriction_Domain import (
            Meal_Dietary_Restriction_Domain,
        )
        from dto.Meal_Dietary_Restriction_DTO import Meal_Dietary_Restriction_DTO

        meal_dietary_restriction_json_file = Path(
            ".", "nutrient_data", "new_meal_dietary_restrictions.json"
        )
        meal_dietary_restrictions_data = load_json(
            filename=meal_dietary_restriction_json_file
        )

        # Only initialize custom values, not USDA values which are initialized alongside Meal_Plan_Models
        for meal_dietary_restriction_json in meal_dietary_restrictions_data:
            meal_dietary_restriction_dto = Meal_Dietary_Restriction_DTO(
                meal_dietary_restriction_json=meal_dietary_restriction_json
            )
            meal_dietary_restriction_domain = Meal_Dietary_Restriction_Domain(
                meal_dietary_restriction_object=meal_dietary_restriction_dto
            )
            meal_dietary_restriction_model = Meal_Dietary_Restriction_Model(
                meal_dietary_restriction_domain=meal_dietary_restriction_domain
            )
            self.db.session.add(meal_dietary_restriction_model)
        self.db.session.commit()
