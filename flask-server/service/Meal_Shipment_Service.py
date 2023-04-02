from domain.Meal_Shipment_Domain import Meal_Shipment_Domain
from uuid import UUID
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from repository.Meal_Shipment_Repository import Meal_Shipment_Repository


class Meal_Shipment_Service(object):
    def __init__(self, meal_shipment_repository: 'Meal_Shipment_Repository') -> None:
        self.meal_shipment_repository = meal_shipment_repository

    def get_meal_shipment(self, meal_subscription_invoice_id: UUID) -> Meal_Shipment_Domain:
        meal_shipment_domain: Meal_Shipment_Domain = Meal_Shipment_Domain(
            meal_shipment_object=self.meal_shipment_repository.get_meal_shipment(meal_subscription_invoice_id=meal_subscription_invoice_id))
        return meal_shipment_domain
