from domain.Meal_Dietary_Restriction_Domain import Meal_Dietary_Restriction_Domain
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from repository.Meal_Dietary_Restriction_Repository import (
        Meal_Dietary_Restriction_Repository,
    )
    from dto.Meal_Dietary_Restriction_DTO import Meal_Dietary_Restriction_DTO


class Meal_Dietary_Restriction_Service(object):
    def __init__(
        self, meal_dietary_restriction_repository: "Meal_Dietary_Restriction_Repository"
    ) -> None:
        self.meal_dietary_restriction_repository = meal_dietary_restriction_repository

    def get_meal_dietary_restrictions(self) -> list[Meal_Dietary_Restriction_Domain]:
        meal_dietary_restriction_domains = [
            Meal_Dietary_Restriction_Domain(meal_dietary_restriction_object=x)
            for x in self.meal_dietary_restriction_repository.get_meal_dietary_restrictions()
        ]
        return meal_dietary_restriction_domains

    def create_meal_dietary_restriction(
        self, meal_dietary_restriction_dto: "Meal_Dietary_Restriction_DTO"
    ) -> None:
        new_meal_dietary_restriction = Meal_Dietary_Restriction_Domain(
            meal_dietary_restriction_object=meal_dietary_restriction_dto
        )
        self.meal_dietary_restriction_repository.create_meal_dietary_restriction(
            meal_dietary_restriction_domain=new_meal_dietary_restriction
        )

    def write_meal_dietary_restrictions(self) -> None:
        from pathlib import Path
        from utils.write_json import write_json

        json_file_path = (
            Path(".")
            .joinpath("nutrient_data")
            .joinpath("new_meal_dietary_restrictions.json")
        )

        with open(json_file_path, "r+") as outfile:
            meal_dietary_restriction_dicts = [
                x.serialize() for x in self.get_meal_dietary_restrictions()
            ]
            write_json(outfile=outfile, dicts=meal_dietary_restriction_dicts)
