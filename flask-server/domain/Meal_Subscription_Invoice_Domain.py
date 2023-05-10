from models import Meal_Subscription_Invoice_Model
from .Base_Domain import Base_Domain
from dto.Meal_Subscription_Invoice_DTO import Meal_Subscription_Invoice_DTO
from uuid import UUID


class Meal_Subscription_Invoice_Domain(Base_Domain):
    def __init__(
        self,
        meal_subscription_invoice_object: Meal_Subscription_Invoice_Model
        | Meal_Subscription_Invoice_DTO,
    ) -> None:
        self.id: UUID = meal_subscription_invoice_object.id
        self.meal_subscription_id: UUID = (
            meal_subscription_invoice_object.meal_subscription_id
        )
        self.subtotal: float = meal_subscription_invoice_object.subtotal
        self.sales_tax_percentage: float = (
            meal_subscription_invoice_object.sales_tax_percentage
        )
        self.sales_tax_total: float = meal_subscription_invoice_object.sales_tax_total
        self.shipping_total: float = meal_subscription_invoice_object.shipping_total
        self.stripe_fee_total: float = meal_subscription_invoice_object.stripe_fee_total
        self.stripe_invoice_id: str = meal_subscription_invoice_object.stripe_invoice_id
        self.stripe_payment_intent_id: str = (
            meal_subscription_invoice_object.stripe_payment_intent_id
        )
        self.total: float = meal_subscription_invoice_object.total
        self.datetime: float = meal_subscription_invoice_object.datetime
        self.delivery_date: float = meal_subscription_invoice_object.delivery_date

    def set_invoice_order_data(self, order_properties: dict) -> None:
        self.subtotal = order_properties["subtotal"]
        self.sales_tax_percentage = order_properties["sales_tax_percentage"]
        self.sales_tax_total = order_properties["sales_tax_total"]
        self.shipping_total = order_properties["shipping_total"]
        self.stripe_fee_total = order_properties["stripe_fee_total"]
        self.total = order_properties["total"]
