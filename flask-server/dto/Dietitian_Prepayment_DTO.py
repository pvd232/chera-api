from .Base_DTO import Base_DTO
from domain.Dietitian_Prepayment_Domain import Dietitian_Prepayment_Domain
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from domain.Dietitian_Prepayment_Domain import Dietitian_Prepayment_Domain


class Dietitian_Prepayment_DTO(Base_DTO):
    def __init__(self, dietitian_prepayment_json: dict, dietitian_prepayment_domain: 'Dietitian_Prepayment_Domain') -> None:
        if dietitian_prepayment_json:
            self.id = dietitian_prepayment_json['id']
            self.dietitian_id = dietitian_prepayment_json['dietitian_id']
            self.staged_client_id = dietitian_prepayment_json['staged_client_id']
            self.subtotal = dietitian_prepayment_json['subtotal']
            self.sales_tax_percentage = dietitian_prepayment_json['sales_tax_percentage']
            self.sales_tax_total = dietitian_prepayment_json['sales_tax_total']
            self.shipping_total = dietitian_prepayment_json['shipping_total']
            self.stripe_fee_total = dietitian_prepayment_json['stripe_fee_total']
            self.stripe_payment_intent_id = dietitian_prepayment_json['stripe_payment_intent_id']
            self.total = dietitian_prepayment_json['total']
            self.datetime = dietitian_prepayment_json['datetime']
        elif dietitian_prepayment_domain:
            self.id = dietitian_prepayment_domain.id
            self.dietitian_id = dietitian_prepayment_domain.dietitian_id
            self.staged_client_id = dietitian_prepayment_domain.staged_client_id
            self.subtotal = dietitian_prepayment_domain.subtotal
            self.sales_tax_percentage = dietitian_prepayment_domain.sales_tax_percentage
            self.sales_tax_total = dietitian_prepayment_domain.sales_tax_total
            self.shipping_total = dietitian_prepayment_domain.shipping_total
            self.stripe_fee_total = dietitian_prepayment_domain.stripe_fee_total
            self.stripe_payment_intent_id = dietitian_prepayment_domain.stripe_payment_intent_id
            self.total = dietitian_prepayment_domain.total
            self.datetime = dietitian_prepayment_domain.datetime
