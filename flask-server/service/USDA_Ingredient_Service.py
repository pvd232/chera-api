from domain.USDA_Ingredient_Domain import USDA_Ingredient_Domain
from domain.Recipe_Ingredient_Domain import Recipe_Ingredient_Domain
import json
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from repository.USDA_Ingredient_Repository import USDA_Ingredient_Repository
    from dto.USDA_Nutrient_Mapper_DTO import USDA_Nutrient_Mapper_DTO


class USDA_Ingredient_Service(object):
    def __init__(self, usda_ingredient_repository: 'USDA_Ingredient_Repository') -> None:
        self.usda_ingredient_repository = usda_ingredient_repository

    def create_usda_ingredient(self, usda_nutrient_mapper_dto: 'USDA_Nutrient_Mapper_DTO') -> None:
        self.usda_ingredient_repository.create_ingredient(
            usda_nutrient_mapper_dto=usda_nutrient_mapper_dto)

    def get_usda_ingredients(self) -> list[USDA_Ingredient_Domain]:
        usda_ingredient_domains: list[USDA_Ingredient_Domain] = [USDA_Ingredient_Domain(
            usda_ingredient_object=x) for x in self.usda_ingredient_repository.get_usda_ingredients()]
        return usda_ingredient_domains

    def get_usda_ingredient(self, usda_ingredient_id: str) -> USDA_Ingredient_Domain:
        return USDA_Ingredient_Domain(usda_ingredient_object=self.usda_ingredient_repository.get_usda_ingredient(usda_ingredient_id=usda_ingredient_id))

    def update_usda_ingredient(self, usda_ingredient_id: str, recipe_ingredient_domain: Recipe_Ingredient_Domain) -> None:
        self.usda_ingredient_repository.update_usda_ingredient(
            usda_ingredient_id=usda_ingredient_id, recipe_ingredient_domain=recipe_ingredient_domain)

    def write_usda_ingredients(self) -> None:
        with open("new_usda_ingredients.json", "r+") as outfile:
            usda_ingredient_dtos = [x.dto_serialize()
                                    for x in self.get_usda_ingredients()]
            data = json.load(outfile)
            if data:
                outfile.seek(0)
                json.dump(usda_ingredient_dtos, outfile, indent=4)
                outfile.truncate()
            else:
                outfile.write(json.dumps(usda_ingredient_dtos, indent=4))
