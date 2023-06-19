from repository.Nutrient_Repository import Nutrient_Repository
from domain.Nutrient_Domain import Nutrient_Domain
from dto.Nutrient_DTO import Nutrient_DTO
import json


class Nutrient_Service(object):
    def __init__(self, nutrient_repository: Nutrient_Repository) -> None:
        self.nutrient_repository = nutrient_repository

    def get_nutrient(self, nutrient_id: str) -> Nutrient_Domain:
        nutrient_domain = Nutrient_Domain(
            nutrient_object=self.nutrient_repository.get_nutrient(
                nutrient_id=nutrient_id
            )
        )
        return nutrient_domain

    def get_nutrients(self) -> list[Nutrient_Domain]:
        nutrient_domains = [
            Nutrient_Domain(nutrient_object=x)
            for x in self.nutrient_repository.get_nutrients()
        ]
        return nutrient_domains

    def write_nutrients(self) -> None:
        from pathlib import Path
        from utils.write_json import write_json

        nutrient_json_file = Path(".", "nutrient_data", "new_nutrients.json")
        with open(nutrient_json_file, "r+") as outfile:
            nutrient_dicts = [
                Nutrient_DTO(nutrient_domain=x).serialize()
                for x in self.get_nutrients()
            ]
            write_json(outfile=outfile, dicts=nutrient_dicts)
