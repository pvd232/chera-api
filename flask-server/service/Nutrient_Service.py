from repository.Nutrient_Repository import Nutrient_Repository
from domain.Nutrient_Domain import Nutrient_Domain
from dto.Nutrient_DTO import Nutrient_DTO
import json


class Nutrient_Service(object):
    def __init__(self, nutrient_repository: Nutrient_Repository) -> None:
        self.nutrient_repository = nutrient_repository

    def get_nutrient(self, nutrient_id: str) -> Nutrient_Domain:
        nutrient_domain = Nutrient_Domain(
            nutrient_object=self.nutrient_repository.get_nutrient(nutrient_id=nutrient_id))
        return nutrient_domain

    def get_nutrients(self) -> list[Nutrient_Domain]:
        nutrient_domains = [Nutrient_Domain(
            nutrient_object=x) for x in self.nutrient_repository.get_nutrients()]
        return nutrient_domains

    def write_nutrients(self) -> None:
        with open("new_nutrients.json", "r+") as outfile:
            nutrient_dtos = [Nutrient_DTO(nutrient_domain=x)
                             for x in self.get_nutrients()]
            serialized_nutrient_DTOs = [x.serialize() for x in nutrient_dtos]
            data = json.load(outfile)
            if data:
                outfile.seek(0)
                json.dump(serialized_nutrient_DTOs, outfile, indent=4)
                outfile.truncate()
            else:
                outfile.write(json.dumps(serialized_nutrient_DTOs, indent=4))
