from domain.Meal_Plan_Domain import Meal_Plan_Domain
from models import load_json
from uuid import UUID
import json
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from repository.Meal_Plan_Repository import Meal_Plan_Repository


class Meal_Plan_Service(object):
    def __init__(self, meal_plan_repository: 'Meal_Plan_Repository') -> None:
        self.meal_plan_repository = meal_plan_repository

    def get_meal_plan(self, meal_plan_id: UUID) -> Meal_Plan_Domain:
        meal_plan = Meal_Plan_Domain(meal_plan_object=self.meal_plan_repository.get_meal_plan(
            meal_plan_id=meal_plan_id))
        return meal_plan

    def get_meal_plans(self) -> list[Meal_Plan_Domain]:

        meal_plan_domains: list[Meal_Plan_Domain] = [Meal_Plan_Domain(
            meal_plan_object=x) for x in self.meal_plan_repository.get_meal_plans()]
        return meal_plan_domains

    def update_meal_plans(self) -> None:
        meal_plan_dicts = load_json("meal_plans.json")
        meal_plan_domains: list[Meal_Plan_Domain] = [Meal_Plan_Domain(
            meal_plan_json=x) for x in meal_plan_dicts]
        self.meal_plan_repository.update_meal_plans(
            new_meal_plans=meal_plan_domains)

    def write_meal_plans(self) -> None:
        with open("new_meal_plans.json", "r+") as outfile:
            meal_plan_dtos = [x.dto_serialize()
                              for x in self.get_meal_plans()]
            data = json.load(outfile)
            if data:
                outfile.seek(0)
                json.dump(meal_plan_dtos, outfile, indent=4)
                outfile.truncate()
            else:
                outfile.write(json.dumps(meal_plan_dtos, indent=4))
