from domain.Meal_Sample_Shipment_Domain import Meal_Sample_Shipment_Domain
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from repository.Meal_Sample_Shipment_Repository import (
        Meal_Sample_Shipment_Repository,
    )


class Meal_Sample_Shipment_Service(object):
    def __init__(
        self, meal_sample_shipment_repository: "Meal_Sample_Shipment_Repository"
    ) -> None:
        self.meal_sample_shipment_repository = meal_sample_shipment_repository

    def get_meal_sample_shipment(
        self, dietitian_id: str
    ) -> Meal_Sample_Shipment_Domain:
        meal_sample_shipment_domain: Meal_Sample_Shipment_Domain = Meal_Sample_Shipment_Domain(
            meal_sample_shipment_object=self.meal_sample_shipment_repository.get_meal_sample_shipment(
                dietitian_id=dietitian_id
            )
        )
        return meal_sample_shipment_domain

    def get_meal_sample_shipments(self) -> list[Meal_Sample_Shipment_Domain]:
        meal_sample_shipment_objects = (
            self.meal_sample_shipment_repository.get_meal_sample_shipments()
        )
        meal_sample_shipment_domains = [
            Meal_Sample_Shipment_Domain(meal_sample_shipment_object=x)
            for x in meal_sample_shipment_objects
        ]
        return meal_sample_shipment_domains

    def write_meal_sample_shipments(self) -> None:
        from pathlib import Path
        from utils.write_json import write_json

        json_file_path = (
            Path(".")
            .joinpath("nutrient_data")
            .joinpath("new_meal_sample_shipments.json")
        )

        with open(json_file_path, "r+") as outfile:
            meal_sample_shipment_dtos = [
                x.serialize() for x in self.get_meal_sample_shipments()
            ]
            write_json(outfile=outfile, dicts=meal_sample_shipment_dtos)
