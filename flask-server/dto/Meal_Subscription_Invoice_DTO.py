from dto.Base_DTO import Base_DTO
from uuid import UUID, uuid4
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from domain.Meal_Subscription_Invoice_Domain import Meal_Subscription_Invoice_Domain


class Meal_Subscription_Invoice_DTO(Base_DTO):
    def __init__(
        self,
        meal_subscription_invoice_json: dict = None,
        meal_subscription_invoice_domain: "Meal_Subscription_Invoice_Domain" = None,
    ) -> None:
        if meal_subscription_invoice_json:
            print("meal_subscription_invoice_json", meal_subscription_invoice_json)
            self.id: UUID = UUID(meal_subscription_invoice_json["id"])
            self.meal_subscription_id: UUID = UUID(
                meal_subscription_invoice_json["meal_subscription_id"]
            )
            self.subtotal: float = float(meal_subscription_invoice_json["subtotal"])
            self.sales_tax_percentage: float = float(
                meal_subscription_invoice_json["sales_tax_percentage"]
            )
            self.sales_tax_total: float = float(
                meal_subscription_invoice_json["sales_tax_total"]
            )
            self.shipping_total: float = float(
                meal_subscription_invoice_json["shipping_total"]
            )
            self.stripe_fee_total: float = float(
                meal_subscription_invoice_json["stripe_fee_total"]
            )
            self.stripe_invoice_id: str = meal_subscription_invoice_json[
                "stripe_invoice_id"
            ]
            self.stripe_payment_intent_id: str = meal_subscription_invoice_json[
                "stripe_payment_intent_id"
            ]
            self.total: float = meal_subscription_invoice_json["total"]
            self.datetime: float = float(meal_subscription_invoice_json["datetime"])
            self.delivery_date: float = float(
                meal_subscription_invoice_json["delivery_date"]
            )
        elif meal_subscription_invoice_domain:
            self.id: UUID = meal_subscription_invoice_domain.id
            self.meal_subscription_id: UUID = (
                meal_subscription_invoice_domain.meal_subscription_id
            )
            self.subtotal: float = meal_subscription_invoice_domain.subtotal
            self.sales_tax_percentage: float = (
                meal_subscription_invoice_domain.sales_tax_percentage
            )
            self.sales_tax_total: float = (
                meal_subscription_invoice_domain.sales_tax_total
            )
            self.shipping_total: float = meal_subscription_invoice_domain.shipping_total
            self.stripe_fee_total: float = (
                meal_subscription_invoice_domain.stripe_fee_total
            )
            self.stripe_invoice_id: str = (
                meal_subscription_invoice_domain.stripe_invoice_id
            )
            self.stripe_payment_intent_id: str = (
                meal_subscription_invoice_domain.stripe_payment_intent_id
            )
            self.total: float = meal_subscription_invoice_domain.total
            self.datetime: float = meal_subscription_invoice_domain.datetime
            self.delivery_date: float = meal_subscription_invoice_domain.delivery_date

        else:
            self.id = uuid4()
            self.meal_subscription_id = ""
            self.subtotal = 0.0
            self.sales_tax_percentage = 0.0
            self.sales_tax_total = 0.0
            self.shipping_total = 0.0
            self.stripe_fee_total = 0.0
            self.stripe_invoice_id = ""
            self.stripe_payment_intent_id = ""
            self.total = 0.0
            self.datetime = 0.0
            self.delivery_date = 0.0
