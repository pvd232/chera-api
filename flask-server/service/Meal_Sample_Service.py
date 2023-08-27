from domain.Meal_Sample_Domain import Meal_Sample_Domain
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from repository.Meal_Sample_Repository import Meal_Sample_Repository
    from dto.Meal_Sample_DTO import Meal_Sample_DTO


class Meal_Sample_Service(object):
    def __init__(self, meal_sample_repository: "Meal_Sample_Repository") -> None:
        self.meal_sample_repository = meal_sample_repository

    def create_meal_samples(self, meal_sample_dtos: list["Meal_Sample_DTO"]) -> None:
        meal_sample_domains = [
            Meal_Sample_Domain(meal_sample_object=x) for x in meal_sample_dtos
        ]
        self.meal_sample_repository.create_meal_samples(
            meal_sample_domains=meal_sample_domains
        )

    def get_meal_samples(
        self,
    ) -> Optional[list[Meal_Sample_Domain]]:
        meal_sample_objects: Optional[
            list["Meal_Sample_Domain"]
        ] = self.meal_sample_repository.get_meal_samples()

        meal_sample_domains: list[Meal_Sample_Domain] = [
            Meal_Sample_Domain(meal_sample_object=x) for x in meal_sample_objects
        ]
        return meal_sample_domains

    def write_meal_samples(self) -> None:
        from pathlib import Path
        from utils.write_json import write_json

        json_file_path = (
            Path(".").joinpath("nutrient_data").joinpath("new_meal_samples.json")
        )

        with open(json_file_path, "r+") as outfile:
            meal_sample_dtos = [x.serialize() for x in self.get_meal_samples()]
            write_json(outfile=outfile, dicts=meal_sample_dtos)
