from domain.Meal_Sample_Shipment_Domain import Meal_Sample_Shipment_Domain
from uuid import UUID
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