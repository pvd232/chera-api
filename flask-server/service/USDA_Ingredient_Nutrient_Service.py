from domain.USDA_Ingredient_Nutrient_Domain import USDA_Ingredient_Nutrient_Domain
import json
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from repository.USDA_Ingredient_Nutrient_Repository import USDA_Ingredient_Nutrient_Repository
    from dto.USDA_Ingredient_Nutrient_DTO import USDA_Ingredient_Nutrient_DTO


class USDA_Ingredient_Nutrient_Service(object):
    def __init__(self, usda_ingredient_nutrient_repository: 'USDA_Ingredient_Nutrient_Repository') -> None:
        self.usda_ingredient_nutrient_repository = usda_ingredient_nutrient_repository

    def create_usda_ingredient_nutrients(self, usda_ingredient_nutrient_dtos: list['USDA_Ingredient_Nutrient_DTO']) -> None:
        usda_ingredient_nutrient_domains = [USDA_Ingredient_Nutrient_Domain(
            usda_ingredient_nutrient_object=x)for x in usda_ingredient_nutrient_dtos]
        self.usda_ingredient_nutrient_repository.create_usda_ingredient_nutrients(
            usda_ingredient_nutrient_domains=usda_ingredient_nutrient_domains)

    def get_usda_ingredient_nutrients(self, usda_ingredient_id: str) -> list[USDA_Ingredient_Nutrient_Domain]:
        usda_ingredient_nutrient_domains: list[USDA_Ingredient_Nutrient_Domain] = [USDA_Ingredient_Nutrient_Domain(
            usda_ingredient_nutrient_object=x) for x in self.usda_ingredient_nutrient_repository.get_usda_ingredient_nutrients(usda_ingredient_id=usda_ingredient_id)]
        return usda_ingredient_nutrient_domains

    def write_usda_ingredient_nutrients(self) -> None:
        with open("new_usda_ingredient_nutrients.json", "r+") as outfile:
            usda_ingredient_nutrient_dtos = [x.dto_serialize()
                                             for x in self.get_usda_ingredient_nutrients()]
            data = json.load(outfile)
            if data:
                outfile.seek(0)
                json.dump(usda_ingredient_nutrient_dtos, outfile, indent=4)
                outfile.truncate()
            else:
                outfile.write(json.dumps(
                    usda_ingredient_nutrient_dtos, indent=4))
