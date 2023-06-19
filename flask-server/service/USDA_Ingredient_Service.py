from domain.USDA_Ingredient_Domain import USDA_Ingredient_Domain
from domain.Recipe_Ingredient_Domain import Recipe_Ingredient_Domain
import json
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from repository.USDA_Ingredient_Repository import USDA_Ingredient_Repository
    from service.USDA_Ingredient_Nutrient_Service import (
        USDA_Ingredient_Nutrient_Service,
    )
    from service.USDA_Ingredient_Portion_Service import USDA_Ingredient_Portion_Service
    from service.USDA_API_Service import USDA_API_Service
    from dto.USDA_Nutrient_Mapper_DTO import USDA_Nutrient_Mapper_DTO
    from domain.Imperial_Unit_Domain import Imperial_Unit_Domain
    from domain.Nutrient_Domain import Nutrient_Domain


class USDA_Ingredient_Service(object):
    def __init__(
        self, usda_ingredient_repository: "USDA_Ingredient_Repository"
    ) -> None:
        self.usda_ingredient_repository = usda_ingredient_repository

    def create_usda_ingredient(
        self, usda_nutrient_mapper_dto: "USDA_Nutrient_Mapper_DTO"
    ) -> None:
        self.usda_ingredient_repository.create_ingredient(
            usda_nutrient_mapper_dto=usda_nutrient_mapper_dto
        )

    def get_usda_ingredients(self) -> list[USDA_Ingredient_Domain]:
        usda_ingredient_domains: list[USDA_Ingredient_Domain] = [
            USDA_Ingredient_Domain(usda_ingredient_object=x)
            for x in self.usda_ingredient_repository.get_usda_ingredients()
        ]
        return usda_ingredient_domains

    def get_usda_ingredient(self, usda_ingredient_id: str) -> USDA_Ingredient_Domain:
        return USDA_Ingredient_Domain(
            usda_ingredient_object=self.usda_ingredient_repository.get_usda_ingredient(
                usda_ingredient_id=usda_ingredient_id
            )
        )

    def update_usda_ingredient(
        self,
        usda_ingredient_id: str,
        recipe_ingredient_domain: Recipe_Ingredient_Domain,
    ) -> None:
        self.usda_ingredient_repository.update_usda_ingredient(
            usda_ingredient_id=usda_ingredient_id,
            recipe_ingredient_domain=recipe_ingredient_domain,
        )

    def write_usda_ingredients(self) -> None:
        from pathlib import Path
        from utils.write_json import write_json

        json_file_path = (
            Path(".").joinpath("nutrient_data").joinpath("new_usda_ingredients.json")
        )
        with open(json_file_path, "r+") as outfile:
            usda_ingredient_dicts = [x.serialize() for x in self.get_usda_ingredients()]
            for ingredient_dict in usda_ingredient_dicts:
                if ingredient_dict["id"] == "olive oil":
                    ingredient_dict["id"] = "olive_oil"
            write_json(outfile=outfile, dicts=usda_ingredient_dicts)

    def recreate_usda_ingredients(
        self,
        imperial_units: list["Imperial_Unit_Domain"],
        nutrients: list["Nutrient_Domain"],
        usda_api_service: "USDA_API_Service",
        usda_ingredient_nutrient_service: "USDA_Ingredient_Nutrient_Service",
        usda_ingredient_portion_service: "USDA_Ingredient_Portion_Service",
    ) -> None:
        from pathlib import Path
        from utils.load_json import load_json
        from dto.USDA_Nutrient_Mapper_DTO import USDA_Nutrient_Mapper_DTO

        usda_ingredient_json_file_name = Path(
            ".", "nutrient_data", "new_usda_ingredients.json"
        )
        usda_ingredient_data = load_json(usda_ingredient_json_file_name)
        for usda_ingredient_json in usda_ingredient_data:
            fdc_id = usda_ingredient_json["fdc_id"]
            print("fdc_id b4 fetch", fdc_id)
            usda_ingredient_id = usda_ingredient_json["id"]
            usda_ingredient_name = usda_ingredient_json["name"]
            usda_ingredient_data = usda_api_service.get_ingredient(fdc_id=fdc_id)
            print("after fetch")
            usda_nutrient_mapper_dto = USDA_Nutrient_Mapper_DTO(
                usda_ingredient_id=usda_ingredient_id,
                usda_ingredient_name=usda_ingredient_name,
                fdc_id=fdc_id,
                usda_ingredient_data=usda_ingredient_data,
                nutrients_list=nutrients,
                imperial_units=imperial_units,
            )
            self.usda_ingredient_repository.create_ingredient(
                usda_nutrient_mapper_dto=usda_nutrient_mapper_dto
            )
            print("after map")

            for nutrient in usda_nutrient_mapper_dto.nutrients:
                usda_ingredient_nutrient_service.create_usda_ingredient_nutrient(
                    usda_ingredient_nutrient_dto=nutrient
                )

            for portion in usda_nutrient_mapper_dto.portions:
                usda_ingredient_portion_service.create_usda_ingredient_portion(
                    usda_ingredient_portion_dto=portion
                )
            print("after add everything")
