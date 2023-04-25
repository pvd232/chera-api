from domain.Meal_Domain import Meal_Domain
from uuid import UUID
import json
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from repository.Meal_Repository import Meal_Repository
    from dto.Meal_DTO import Meal_DTO


class Meal_Service(object):
    def __init__(self, meal_repository: 'Meal_Repository') -> None:
        self.meal_repository = meal_repository

    def get_meals(self) -> list[Meal_Domain]:
        meal_domains: list[Meal_Domain] = [Meal_Domain(
            meal_object=x) for x in self.meal_repository.get_meals()]
        return meal_domains

    def get_meal(self, meal_id: UUID) -> Optional[Meal_Domain]:
        requested_meal_domain = self.meal_repository.get_meal(
            meal_id=meal_id)
        if requested_meal_domain:
            meal_domain = Meal_Domain(meal_object=requested_meal_domain)
        return meal_domain

    def create_meal(self, meal_dto: 'Meal_DTO') -> None:
        meal_domain = Meal_Domain(meal_object=meal_dto)
        self.meal_repository.create_meal(meal_domain=meal_domain)
        return

    def write_meals(self) -> None:
        with open("new_meals.json", "r+") as outfile:
            meal_dtos = [x.dto_serialize()
                         for x in self.get_meals()]
            data = json.load(outfile)
            if data:
                outfile.seek(0)
                json.dump(meal_dtos, outfile, indent=4)
                outfile.truncate()
            else:
                outfile.write(json.dumps(meal_dtos, indent=4))
