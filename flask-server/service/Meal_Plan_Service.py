from domain.Meal_Plan_Domain import Meal_Plan_Domain
from models import load_json
from uuid import UUID
import json
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from repository.Meal_Plan_Repository import Meal_Plan_Repository


class Meal_Plan_Service(object):
    def __init__(self, meal_plan_repository: "Meal_Plan_Repository") -> None:
        self.meal_plan_repository = meal_plan_repository

    def get_meal_plan(self, meal_plan_id: UUID) -> Meal_Plan_Domain:
        meal_plan = Meal_Plan_Domain(
            meal_plan_object=self.meal_plan_repository.get_meal_plan(
                meal_plan_id=meal_plan_id
            )
        )
        return meal_plan

    def get_meal_plans(self) -> list[Meal_Plan_Domain]:
        meal_plan_domains: list[Meal_Plan_Domain] = [
            Meal_Plan_Domain(meal_plan_object=x)
            for x in self.meal_plan_repository.get_meal_plans()
        ]
        return meal_plan_domains

    def write_meal_plans(self) -> None:
        from pathlib import Path
        from utils.write_json import write_json

        meal_plan_json_file = Path(".", "nutrient_data", "new_meal_plans.json")
        with open(meal_plan_json_file, "r+") as outfile:
            meal_plan_dicts = [x.serialize() for x in self.get_meal_plans()]
            write_json(outfile=outfile, dicts=meal_plan_dicts)
