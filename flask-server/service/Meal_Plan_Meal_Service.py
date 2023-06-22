from domain.Meal_Plan_Meal_Domain import Meal_Plan_Meal_Domain

from uuid import UUID
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from repository.Meal_Plan_Meal_Repository import Meal_Plan_Meal_Repository
    from service.Meal_Plan_Service import Meal_Plan_Service
    from models import Meal_Plan_Meal_Model
    from dto.Meal_Plan_Meal_DTO import Meal_Plan_Meal_DTO


class Meal_Plan_Meal_Service(object):
    def __init__(self, meal_plan_meal_repository: "Meal_Plan_Meal_Repository") -> None:
        self.meal_plan_meal_repository = meal_plan_meal_repository

    def get_meal_plan_meal(
        self, meal_plan_meal_id: UUID
    ) -> Optional[Meal_Plan_Meal_Domain]:
        meal_plan_meal: Optional[
            Meal_Plan_Meal_Model
        ] = self.meal_plan_meal_repository.get_meal_plan_meal(
            meal_plan_meal_id=meal_plan_meal_id
        )
        meal_plan_meal_domain: Meal_Plan_Meal_Domain = Meal_Plan_Meal_Domain(
            meal_plan_meal_object=meal_plan_meal
        )
        return meal_plan_meal_domain

    def get_even_meal_plan_meal(
        self, meal_id: UUID, meal_plan_id: UUID
    ) -> Meal_Plan_Meal_Domain:
        even_meal_plan_meal = Meal_Plan_Meal_Domain(
            meal_plan_meal_object=self.meal_plan_meal_repository.get_meal_plan_meal(
                meal_id=meal_id, meal_plan_id=meal_plan_id
            )
        )
        return even_meal_plan_meal

    def get_meal_plan_meals(
        self, meal_plan_id: UUID = None
    ) -> Optional[list[Meal_Plan_Meal_Domain]]:
        meal_plan_meals = self.meal_plan_meal_repository.get_meal_plan_meals(
            meal_plan_id=meal_plan_id
        )
        meal_plan_meal_domains: list[Meal_Plan_Meal_Domain] = [
            Meal_Plan_Meal_Domain(meal_plan_meal_object=x) for x in meal_plan_meals
        ]
        return meal_plan_meal_domains

    def create_meal_plan_meal(self, meal_plan_meal_dto: "Meal_Plan_Meal_DTO") -> None:
        meal_plan_meal_domain: Meal_Plan_Meal_Domain = Meal_Plan_Meal_Domain(
            meal_plan_meal_object=meal_plan_meal_dto
        )
        self.meal_plan_meal_repository.create_meal_plan_meal(
            meal_plan_meal_domain=meal_plan_meal_domain
        )
        return

    def update_meal_plan_meal(
        self,
        meal_plan_meal_dto: "Meal_Plan_Meal_DTO",
        should_update_even: bool,
        meal_plan_service: "Meal_Plan_Service" = None,
    ) -> None:
        odd_meal_plan_meal_domain: Meal_Plan_Meal_Domain = Meal_Plan_Meal_Domain(
            meal_plan_meal_object=meal_plan_meal_dto
        )
        if should_update_even:
            even_meal_plan = meal_plan_service.get_even_meal_plan(
                odd_meal_plan_id=odd_meal_plan_meal_domain.meal_plan_id
            )
            even_meal_plan_meal = self.get_even_meal_plan_meal(
                meal_id=odd_meal_plan_meal_domain.meal_id,
                meal_plan_id=even_meal_plan.id,
            )
            self.meal_plan_meal_repository.update_meal_plan_meal(
                odd_meal_plan_meal_domain=odd_meal_plan_meal_domain,
                even_meal_plan_meal_domain=even_meal_plan_meal,
            )
        else:
            self.meal_plan_meal_repository.update_meal_plan_meal(
                odd_meal_plan_meal_domain=odd_meal_plan_meal_domain,
                even_meal_plan_meal_domain=None,
            )
        return

    def write_meal_plan_meals(self) -> None:
        from pathlib import Path
        from utils.write_json import write_json

        meal_plan_meal_json_file = Path(
            ".", "nutrient_data", "new_meal_plan_meals.json"
        )
        with open(meal_plan_meal_json_file, "r+") as outfile:
            meal_plan_meal_dtos = [x.serialize() for x in self.get_meal_plan_meals()]
            write_json(outfile=outfile, dicts=meal_plan_meal_dtos)
