from domain.USDA_Ingredient_Nutrient_Domain import USDA_Ingredient_Nutrient_Domain
import json
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from repository.USDA_Ingredient_Nutrient_Repository import (
        USDA_Ingredient_Nutrient_Repository,
    )
    from dto.USDA_Ingredient_Nutrient_DTO import USDA_Ingredient_Nutrient_DTO


class USDA_Ingredient_Nutrient_Service(object):
    def __init__(
        self, usda_ingredient_nutrient_repository: "USDA_Ingredient_Nutrient_Repository"
    ) -> None:
        self.usda_ingredient_nutrient_repository = usda_ingredient_nutrient_repository

    def create_usda_ingredient_nutrient(
        self,
        usda_ingredient_nutrient_dto: "USDA_Ingredient_Nutrient_DTO",
    ) -> None:
        self.usda_ingredient_nutrient_repository.create_usda_ingredient_nutrient(
            usda_ingredient_nutrient_dto=usda_ingredient_nutrient_dto
        )

    def create_usda_ingredient_nutrients(
        self, usda_ingredient_nutrient_dtos: list["USDA_Ingredient_Nutrient_DTO"]
    ) -> None:
        usda_ingredient_nutrient_domains = [
            USDA_Ingredient_Nutrient_Domain(usda_ingredient_nutrient_object=x)
            for x in usda_ingredient_nutrient_dtos
        ]
        self.usda_ingredient_nutrient_repository.create_usda_ingredient_nutrients(
            usda_ingredient_nutrient_domains=usda_ingredient_nutrient_domains
        )

    def get_usda_ingredient_nutrients(
        self, usda_ingredient_id: str
    ) -> list[USDA_Ingredient_Nutrient_Domain]:
        usda_ingredient_nutrient_domains: list[USDA_Ingredient_Nutrient_Domain] = [
            USDA_Ingredient_Nutrient_Domain(usda_ingredient_nutrient_object=x)
            for x in self.usda_ingredient_nutrient_repository.get_usda_ingredient_nutrients(
                usda_ingredient_id=usda_ingredient_id
            )
        ]
        return usda_ingredient_nutrient_domains

    def get_all_usda_ingredient_nutrients(
        self,
    ) -> list[USDA_Ingredient_Nutrient_Domain]:
        return [
            USDA_Ingredient_Nutrient_Domain(usda_ingredient_nutrient_object=x)
            for x in self.usda_ingredient_nutrient_repository.get_all_usda_ingredient_nutrients()
        ]

    def write_usda_ingredient_nutrients(self) -> None:
        from pathlib import Path
        from utils.write_json import write_json

        json_file_path = Path(
            ".", "nutrient_data", "new_usda_ingredient_nutrients.json"
        )

        with open(json_file_path, "r+") as outfile:
            usda_ingredient_nutrient_dicts = [
                x.serialize() for x in self.get_all_usda_ingredient_nutrients()
            ]
            for usda_ingredient_nutrient_dict in usda_ingredient_nutrient_dicts:
                if usda_ingredient_nutrient_dict["usda_ingredient_id"] == "olive oil":
                    usda_ingredient_nutrient_dict["usda_ingredient_id"] = "olive_oil"
            write_json(outfile=outfile, dicts=usda_ingredient_nutrient_dicts)
