from models import Meal_Sample_Shipment_Model
from .Base_Domain import Base_Domain
from typing import Optional


class Meal_Sample_Shipment_Domain(Base_Domain):
    def __init__(
        self,
        meal_sample_shipment_object: Optional[Meal_Sample_Shipment_Model] = None,
        meal_sample_shipment_json: Optional[dict] = None,
    ) -> None:
        if meal_sample_shipment_object:
            self.id = meal_sample_shipment_object.id
            self.dietitian_id = meal_sample_shipment_object.dietitian_id
            self.shippo_transaction_id = (
                meal_sample_shipment_object.shippo_transaction_id
            )
            self.label_url = meal_sample_shipment_object.shippo_transaction_id
            self.tracking_number = meal_sample_shipment_object.tracking_number
            self.tracking_url = meal_sample_shipment_object.tracking_url
        elif meal_sample_shipment_json:
            self.id = meal_sample_shipment_json["id"]
            self.dietitian_id = meal_sample_shipment_json["dietitian_id"]
            self.shippo_transaction_id = meal_sample_shipment_json[
                "shippo_transaction_id"
            ]
            self.label_url = meal_sample_shipment_json["shippo_transaction_id"]
            self.tracking_number = meal_sample_shipment_json["tracking_number"]
            self.tracking_url = meal_sample_shipment_json["tracking_url"]
