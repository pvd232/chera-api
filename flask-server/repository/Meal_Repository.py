from repository.Base_Repository import Base_Repository
from models import Meal_Model
from uuid import UUID
from typing import Optional, TYPE_CHECKING
from sqlalchemy import or_

if TYPE_CHECKING:
    from domain.Meal_Domain import Meal_Domain


class Meal_Repository(Base_Repository):
    def get_meal(self, meal_id: UUID) -> Optional[Meal_Model]:
        meal = (
            self.db.session.query(Meal_Model).filter(Meal_Model.id == meal_id).first()
        )
        return meal

    def get_meals(self) -> Optional[list[Meal_Model]]:
        meals = self.db.session.query(Meal_Model).all()
        return meals

    def get_meal_samples(self) -> Optional[list[Meal_Model]]:
        meal_samples = (
            self.db.session.query(Meal_Model)
            .filter(
                or_(
                    Meal_Model.name == "Chicken Pesto Pasta",
                    Meal_Model.name == "Peanut Noodles with Tofu",
                )
            )
            .all()
        )
        return meal_samples

    def create_meal(self, meal_domain: "Meal_Domain") -> None:
        new_meal_model = Meal_Model(meal_domain=meal_domain)
        self.db.session.add(new_meal_model)
        self.db.session.commit()
        return

    def initialize_meals(self) -> None:
        from pathlib import Path
        from utils.load_json import load_json
        from domain.Meal_Domain import Meal_Domain
        from dto.Meal_DTO import Meal_DTO

        meal_json_file = Path(".", "nutrient_data", "new_meals.json")
        meals_data = load_json(filename=meal_json_file)

        # Only initialize custom values, not USDA values which are initialized alongside Meal_Models
        for meal_json in meals_data:
            meal_dto = Meal_DTO(meal_json=meal_json)
            meal_domain = Meal_Domain(meal_object=meal_dto)

            new_meal_model = Meal_Model(meal_domain=meal_domain)
            self.db.session.add(new_meal_model)
        self.db.session.commit()

    def initialize_meal(self, meal_name: str) -> None:
        from pathlib import Path
        from utils.load_json import load_json
        from domain.Meal_Domain import Meal_Domain
        from dto.Meal_DTO import Meal_DTO

        meal_json_file = Path(".", "nutrient_data", "new_meals.json")
        meals_data = load_json(filename=meal_json_file)

        # Only initialize custom values, not USDA values which are initialized alongside Meal_Models
        for meal_json in meals_data:
            if meal_json["name"] == meal_name:
                meal_dto = Meal_DTO(meal_json=meal_json)
                meal_domain = Meal_Domain(meal_object=meal_dto)

                new_meal_model = Meal_Model(meal_domain=meal_domain)
                self.db.session.add(new_meal_model)
        self.db.session.commit()
