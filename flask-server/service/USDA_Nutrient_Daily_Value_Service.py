from domain.USDA_Nutrient_Daily_Value_Domain import USDA_Nutrient_Daily_Value_Domain
from uuid import UUID
import json
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from repository.USDA_Nutrient_Daily_Value_Repository import (
        USDA_Nutrient_Daily_Value_Repository,
    )


class USDA_Nutrient_Daily_Value_Service(object):
    def __init__(
        self,
        usda_nutrient_daily_value_repository: "USDA_Nutrient_Daily_Value_Repository",
    ) -> None:
        self.usda_nutrient_daily_value_repository = usda_nutrient_daily_value_repository

    def get_get_usda_nutrient_daily_values(
        self,
    ) -> list[USDA_Nutrient_Daily_Value_Domain]:
        usda_nutrient_daily_value_domains = [
            USDA_Nutrient_Daily_Value_Domain(usda_nutrient_daily_value_object=x)
            for x in self.usda_nutrient_daily_value_repository.get_usda_nutrient_daily_values()
        ]
        return usda_nutrient_daily_value_domains

    def get_usda_nutrient_daily_value(
        self, meal_plan_id: UUID, nutrient_id: str
    ) -> USDA_Nutrient_Daily_Value_Domain:
        usda_nutrient_daily_value_domain = USDA_Nutrient_Daily_Value_Domain(
            usda_nutrient_daily_value_object=self.usda_nutrient_daily_value_repository.get_usda_nutrient_daily_value(
                meal_plan_id=meal_plan_id, nutrient_id=nutrient_id
            )
        )
        return usda_nutrient_daily_value_domain

    def write_usda_nutrient_daily_values(self) -> None:
        from pathlib import Path
        from utils.write_json import write_json

        usda_daily_value_json_file = Path(
            ".", "nutrient_data", "new_usda_nutrient_daily_values.json"
        )
        with open(usda_daily_value_json_file, "r+") as outfile:
            usda_nutrient_daily_value_dicts = [
                x.serialize() for x in self.get_get_usda_nutrient_daily_values()
            ]
            write_json(outfile=outfile, dicts=usda_nutrient_daily_value_dicts)
