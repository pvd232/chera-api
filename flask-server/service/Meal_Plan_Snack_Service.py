from domain.Meal_Plan_Snack_Domain import Meal_Plan_Snack_Domain
from domain.Meal_Plan_Domain import Meal_Plan_Domain
from domain.Recipe_Ingredient_Domain import Recipe_Ingredient_Domain

from uuid import UUID
import json
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from repository.Meal_Plan_Snack_Repository import Meal_Plan_Snack_Repository
    from models import Meal_Plan_Snack_Model
    from dto.Meal_Plan_Snack_DTO import Meal_Plan_Snack_DTO


class Meal_Plan_Snack_Service(object):
    def __init__(
        self, meal_plan_snack_repository: "Meal_Plan_Snack_Repository"
    ) -> None:
        self.meal_plan_snack_repository = meal_plan_snack_repository

    def get_meal_plan_snack(
        self, meal_plan_snack_id: UUID
    ) -> Optional[Meal_Plan_Snack_Domain]:
        meal_plan_snack: Optional[
            Meal_Plan_Snack_Model
        ] = self.meal_plan_snack_repository.get_meal_plan_snack(
            meal_plan_snack_id=meal_plan_snack_id
        )
        meal_plan_snack_domain: Meal_Plan_Snack_Domain = Meal_Plan_Snack_Domain(
            meal_plan_snack_object=meal_plan_snack
        )
        return meal_plan_snack_domain

    def get_meal_plan_snacks(
        self, meal_plan_id: UUID = None
    ) -> Optional[list[Meal_Plan_Snack_Domain]]:
        meal_plan_snacks: Optional[
            list[Meal_Plan_Snack_Model]
        ] = self.meal_plan_snack_repository.get_meal_plan_snacks(
            meal_plan_id=meal_plan_id
        )
        if meal_plan_snacks:
            meal_plan_snack_domains: list[Meal_Plan_Snack_Domain] = [
                Meal_Plan_Snack_Domain(meal_plan_snack_object=x)
                for x in meal_plan_snacks
            ]
            return meal_plan_snack_domains
        else:
            return False

    def get_standard_meal_plan_snacks(self):
        meal_plan_snacks = (
            self.meal_plan_snack_repository.get_standard_meal_plan_snacks()
        )
        meal_plan_snack_domains: list[Meal_Plan_Snack_Domain] = [
            Meal_Plan_Snack_Domain(meal_plan_snack_object=x) for x in meal_plan_snacks
        ]
        return meal_plan_snack_domains

    def create_meal_plan_snack(
        self, meal_plan_snack_dto: "Meal_Plan_Snack_DTO"
    ) -> None:
        meal_plan_snack_domain: Meal_Plan_Snack_Domain = Meal_Plan_Snack_Domain(
            meal_plan_snack_object=meal_plan_snack_dto
        )
        self.meal_plan_snack_repository.create_meal_plan_snack(
            meal_plan_snack_domain=meal_plan_snack_domain
        )
        return

    def update_meal_plan_snack(
        self,
        meal_plan_snack_dto: "Meal_Plan_Snack_DTO",
    ) -> None:
        meal_plan_snack_domain = Meal_Plan_Snack_Domain(
            meal_plan_snack_object=meal_plan_snack_dto
        )
        self.meal_plan_snack_repository.update_meal_plan_snack(
            meal_plan_snack_domain=meal_plan_snack_domain
        )

    def write_meal_plan_snacks(self) -> None:
        from pathlib import Path
        from utils.write_json import write_json

        meal_plan_snack_json_file = Path(
            ".", "nutrient_data", "new_meal_plan_snacks.json"
        )
        with open(meal_plan_snack_json_file, "r+") as outfile:
            meal_plan_snack_dtos = [x.serialize() for x in self.get_meal_plan_snacks()]
            write_json(outfile=outfile, dicts=meal_plan_snack_dtos)
