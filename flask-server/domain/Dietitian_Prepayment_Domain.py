from .Base_Domain import Base_Domain
from models import Dietitian_Prepayment_Model
from dto.Dietitian_Prepayment_DTO import Dietitian_Prepayment_DTO


class Dietitian_Prepayment_Domain(Base_Domain):
    def __init__(self, dietitian_prepayment_object: Dietitian_Prepayment_Model | Dietitian_Prepayment_DTO) -> None:
        self.id = dietitian_prepayment_object.id
        self.dietitian_id = dietitian_prepayment_object.dietitian_id
        self.staged_client_id = dietitian_prepayment_object.staged_client_id
        self.subtotal = dietitian_prepayment_object.subtotal
        self.sales_tax_percentage = dietitian_prepayment_object.sales_tax_percentage
        self.sales_tax_total = dietitian_prepayment_object.sales_tax_total
        self.shipping_total = dietitian_prepayment_object.shipping_total
        self.stripe_fee_total = dietitian_prepayment_object.stripe_fee_total
        self.stripe_payment_intent_id = dietitian_prepayment_object.stripe_payment_intent_id
        self.total = dietitian_prepayment_object.total
        self.datetime = dietitian_prepayment_object.datetime
