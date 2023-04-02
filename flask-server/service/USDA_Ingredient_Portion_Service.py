from domain.USDA_Ingredient_Portion_Domain import USDA_Ingredient_Portion_Domain
from uuid import UUID
import json
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from repository.USDA_Ingredient_Portion_Repository import USDA_Ingredient_Portion_Repository


class USDA_Ingredient_Portion_Service(object):
    def __init__(self, usda_ingredient_portion_repository: 'USDA_Ingredient_Portion_Repository') -> None:
        self.usda_ingredient_portion_repository = usda_ingredient_portion_repository

    def get_usda_ingredient_portion(self, usda_ingredient_portion_id: UUID) -> USDA_Ingredient_Portion_Domain:
        usda_ingredient_portion = self.usda_ingredient_portion_repository.get_usda_ingredient_portion(
            usda_ingredient_portion_id=usda_ingredient_portion_id)
        usda_ingredient_portion_domain = USDA_Ingredient_Portion_Domain(
            usda_ingredient_portion_object=usda_ingredient_portion)
        return usda_ingredient_portion_domain

    def write_usda_ingredient_portions(self) -> None:
        with open("new_usda_ingredient_portions.json", "r+") as outfile:
            usda_ingredient_portion_dtos = [x.dto_serialize()
                                            for x in self.get_usda_ingredient_portions()]
            data = json.load(outfile)
            if data:
                outfile.seek(0)
                json.dump(usda_ingredient_portion_dtos, outfile, indent=4)
                outfile.truncate()
            else:
                outfile.write(json.dumps(
                    usda_ingredient_portion_dtos, indent=4))
