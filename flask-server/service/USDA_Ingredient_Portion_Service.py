from domain.USDA_Ingredient_Portion_Domain import USDA_Ingredient_Portion_Domain
from uuid import UUID
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from repository.USDA_Ingredient_Portion_Repository import (
        USDA_Ingredient_Portion_Repository,
    )
    from dto.USDA_Ingredient_Portion_DTO import USDA_Ingredient_Portion_DTO


class USDA_Ingredient_Portion_Service(object):
    def __init__(
        self, usda_ingredient_portion_repository: "USDA_Ingredient_Portion_Repository"
    ) -> None:
        self.usda_ingredient_portion_repository = usda_ingredient_portion_repository

    def get_usda_ingredient_portions(self) -> list[USDA_Ingredient_Portion_Domain]:
        usda_ingredient_portion_domains = [
            USDA_Ingredient_Portion_Domain(usda_ingredient_portion_object=x)
            for x in self.usda_ingredient_portion_repository.get_usda_ingredient_portions()
        ]
        return usda_ingredient_portion_domains

    def create_usda_ingredient_portion(
        self, usda_ingredient_portion_dto: "USDA_Ingredient_Portion_DTO"
    ) -> None:
        usda_ingredient_portion_domain = USDA_Ingredient_Portion_Domain(
            usda_ingredient_portion_object=usda_ingredient_portion_dto
        )
        if (
            usda_ingredient_portion_domain.custom_value == True
            and usda_ingredient_portion_domain.non_metric_unit != "oz"
            and usda_ingredient_portion_domain.fda_portion_id != ""
        ):
            dependent_portion = (
                self.usda_ingredient_portion_repository.get_usda_ingredient_portion(
                    fda_portion_id=usda_ingredient_portion_domain.fda_portion_id
                )
            )
            grams_per_non_metric_unit = (
                dependent_portion.grams_per_non_metric_unit
                * usda_ingredient_portion_domain.multiplier
            )

            usda_ingredient_portion_domain.grams_per_non_metric_unit = (
                grams_per_non_metric_unit
            )
        self.usda_ingredient_portion_repository.create_usda_ingredient_portion(
            usda_ingredient_portion_domain=usda_ingredient_portion_domain
        )

    def update_usda_ingredient_portion(
        self, usda_ingredient_portion_data: dict
    ) -> None:
        dependent_portion = (
            self.usda_ingredient_portion_repository.get_usda_ingredient_portion(
                fda_portion_id=usda_ingredient_portion_data["fda_portion_id"]
            )
        )
        grams_per_non_metric_unit = (
            dependent_portion.grams_per_non_metric_unit
            * usda_ingredient_portion_data["multiplier"]
        )
        usda_ingredient_portion_data[
            "grams_per_non_metric_unit"
        ] = grams_per_non_metric_unit
        self.usda_ingredient_portion_repository.update_usda_ingredient_portion(
            usda_ingredient_portion_data=usda_ingredient_portion_data
        )

    def get_usda_ingredient_portion(
        self, usda_ingredient_portion_id: UUID
    ) -> USDA_Ingredient_Portion_Domain:
        usda_ingredient_portion = (
            self.usda_ingredient_portion_repository.get_usda_ingredient_portion(
                usda_ingredient_portion_id=usda_ingredient_portion_id
            )
        )
        usda_ingredient_portion_domain = USDA_Ingredient_Portion_Domain(
            usda_ingredient_portion_object=usda_ingredient_portion
        )
        return usda_ingredient_portion_domain

    def delete_usda_ingredient_portions(self, usda_ingredient_id: str) -> None:
        self.usda_ingredient_portion_repository.delete_usda_ingredient_portions(
            usda_ingredient_id=usda_ingredient_id
        )

    def write_usda_ingredient_portions(self) -> None:
        from pathlib import Path
        from utils.write_json import write_json

        usda_ingredient_portion_file_name = Path(
            ".", "nutrient_data", "new_usda_ingredient_portions.json"
        )
        with open(usda_ingredient_portion_file_name, "r+") as outfile:
            usda_ingredient_portion_dicts = [
                x.serialize() for x in self.get_usda_ingredient_portions()
            ]
            for usda_ingredient_portion_dict in usda_ingredient_portion_dicts:
                if usda_ingredient_portion_dict["usda_ingredient_id"] == "olive oil":
                    usda_ingredient_portion_dict["usda_ingredient_id"] = "olive_oil"
            write_json(outfile=outfile, dicts=usda_ingredient_portion_dicts)
