from models import Meal_Shipment_Model
from .Base_Domain import Base_Domain


class Meal_Shipment_Domain(Base_Domain):
    def __init__(self, meal_shipment_object: Meal_Shipment_Model = None, meal_shipment_json: dict = None) -> None:
        if meal_shipment_object:
            self.id = meal_shipment_object.id
            self.meal_subscription_invoice_id = meal_shipment_object.meal_subscription_invoice_id
            self.shippo_transaction_id = meal_shipment_object.shippo_transaction_id
            self.label_url = meal_shipment_object.shippo_transaction_id
            self.tracking_number = meal_shipment_object.tracking_number
            self.tracking_url = meal_shipment_object.tracking_url
        elif meal_shipment_json:
            self.id = meal_shipment_json["id"]
            self.meal_subscription_invoice_id = meal_shipment_json["meal_subscription_invoice_id"]
            self.shippo_transaction_id = meal_shipment_json["shippo_transaction_id"]
            self.label_url = meal_shipment_json["shippo_transaction_id"]
            self.tracking_number = meal_shipment_json["tracking_number"]
            self.tracking_url = meal_shipment_json["tracking_url"]
