from domain.Meal_Subscription_Invoice_Domain import Meal_Subscription_Invoice_Domain
from uuid import UUID
from typing import Optional, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from models import Meal_Subscription_Invoice_Model
    from repository.Meal_Subscription_Invoice_Repository import (
        Meal_Subscription_Invoice_Repository,
    )
    from service.Order_Calc_Service import Order_Calc_Service
    from domain.Meal_Subscription_Domain import Meal_Subscription_Domain
    from dto.Meal_Subscription_Invoice_DTO import Meal_Subscription_Invoice_DTO


class Meal_Subscription_Invoice_Service(object):
    def __init__(
        self,
        meal_subscription_invoice_repository: "Meal_Subscription_Invoice_Repository",
    ) -> None:
        self.stripe_fixed_fee = 0.3
        self.stripe_percentage_fee = 0.029
        self.meal_subscription_invoice_repository = meal_subscription_invoice_repository

    def get_upcoming_meal_subscription_invoices(
        self, delivery_date: datetime
    ) -> list[Meal_Subscription_Invoice_Domain]:
        upcoming_meal_subscription_invoices = self.meal_subscription_invoice_repository.get_upcoming_meal_subscription_invoices(
            delivery_date=delivery_date
        )

        upcoming_meal_subscription_invoice_domains = [
            Meal_Subscription_Invoice_Domain(meal_subscription_invoice_object=x)
            for x in upcoming_meal_subscription_invoices
        ]
        return upcoming_meal_subscription_invoice_domains

    def get_meal_subscription_invoice(
        self,
        meal_subscription_invoice_id: Optional[UUID] = None,
        stripe_payment_intent_id: Optional[str] = None,
    ) -> Optional[Meal_Subscription_Invoice_Domain]:
        if meal_subscription_invoice_id:
            return (
                self.meal_subscription_invoice_repository.get_meal_subscription_invoice(
                    meal_subscription_invoice_id=meal_subscription_invoice_id
                )
            )
        elif stripe_payment_intent_id:
            return (
                self.meal_subscription_invoice_repository.get_meal_subscription_invoice(
                    stripe_payment_intent_id=stripe_payment_intent_id
                )
            )

    def get_meal_subscription_invoices(
        self, meal_subscription_id: UUID
    ) -> Optional[list[Meal_Subscription_Invoice_Domain]]:
        meal_subscription_invoices: Optional[
            list["Meal_Subscription_Invoice_Model"]
        ] = self.meal_subscription_invoice_repository.get_meal_subscription_invoices(
            meal_subscription_id=meal_subscription_id
        )
        if meal_subscription_invoices:
            meal_subscription_invoice_domains = [
                Meal_Subscription_Invoice_Domain(meal_subscription_invoice_object=x)
                for x in meal_subscription_invoices
            ]
            return meal_subscription_invoice_domains
        else:
            return None

    def get_first_meal_subscription_invoice(
        self, meal_subscription_id: UUID
    ) -> Optional["Meal_Subscription_Invoice_Domain"]:
        def get_date(
            meal_subscription_invoice: "Meal_Subscription_Invoice_Domain",
        ) -> datetime:
            return meal_subscription_invoice.datetime

        meal_subscription_invoices = self.get_meal_subscription_invoices(
            meal_subscription_id=meal_subscription_id
        )
        if meal_subscription_invoices:
            # sort in ascending order, which will return more recent dates first (larger gap in time since 1970), and older dates last
            meal_subscription_invoices.sort(key=get_date)
            first_created_meal_subscription_invoice: (
                Meal_Subscription_Invoice_Domain
            ) = meal_subscription_invoices[-1]
            return first_created_meal_subscription_invoice
        else:
            return None

    def create_meal_subscription_invoice(
        self,
        meal_subscription_invoice_dto: "Meal_Subscription_Invoice_DTO",
        meal_price: float,
        shipping_cost: float,
        num_items: int,
        order_calc_service: "Order_Calc_Service",
        discount_percentage: Optional[float] = None,
    ) -> Meal_Subscription_Invoice_Domain:
        meal_subscription_invoice_domain = Meal_Subscription_Invoice_Domain(
            meal_subscription_invoice_object=meal_subscription_invoice_dto
        )

        invoice_order_data = order_calc_service.get_order_calc(
            num_items=num_items,
            meal_price=meal_price,
            shipping_cost=shipping_cost,
            discount_percentage=discount_percentage,
        )

        meal_subscription_invoice_domain.set_invoice_order_data(
            order_properties=invoice_order_data
        )

        created_meal_subscription_invoice: "Meal_Subscription_Invoice_Model" = (
            self.meal_subscription_invoice_repository.create_meal_subscription_invoice(
                meal_subscription_invoice_domain=meal_subscription_invoice_domain
            )
        )

        created_meal_subscription_invoice_domain: Meal_Subscription_Invoice_Domain = (
            Meal_Subscription_Invoice_Domain(
                meal_subscription_invoice_object=created_meal_subscription_invoice
            )
        )
        return created_meal_subscription_invoice_domain

    def create_meal_subscription_invoice_from_stripe_event(
        self,
        meal_subscription_invoice_dto: "Meal_Subscription_Invoice_DTO",
        meal_subscription: "Meal_Subscription_Domain",
        stripe_invoice_id: str,
        stripe_payment_intent_id: str,
        meal_price: float,
        shipping_cost: float,
        num_items: int,
        order_calc_service: "Order_Calc_Service",
    ) -> Meal_Subscription_Invoice_Domain:
        new_meal_subscription_invoice_domain = Meal_Subscription_Invoice_Domain(
            meal_subscription_invoice_object=meal_subscription_invoice_dto
        )
        new_meal_subscription_invoice_domain.meal_subscription_id = meal_subscription.id
        new_meal_subscription_invoice_domain.stripe_invoice_id = stripe_invoice_id
        new_meal_subscription_invoice_domain.stripe_payment_intent_id = (
            stripe_payment_intent_id
        )

        invoice_order_data = order_calc_service.get_order_calc(
            num_items=num_items,
            meal_price=meal_price,
            shipping_cost=shipping_cost,
            discount_percentage=False,
        )

        new_meal_subscription_invoice_domain.set_invoice_order_data(
            order_properties=invoice_order_data
        )

        created_meal_subscription_invoice = (
            self.meal_subscription_invoice_repository.create_meal_subscription_invoice(
                meal_subscription_invoice_domain=new_meal_subscription_invoice_domain
            )
        )

        created_meal_subscription_invoice_domain: Meal_Subscription_Invoice_Domain = (
            Meal_Subscription_Invoice_Domain(
                meal_subscription_invoice_object=created_meal_subscription_invoice
            )
        )
        return created_meal_subscription_invoice_domain

    def update_first_meal_subscription_invoice(
        self,
        meal_subscription_invoice_id: UUID,
        stripe_payment_intent_id: str,
        stripe_invoice_id: str,
    ) -> None:
        self.meal_subscription_invoice_repository.update_first_meal_subscription_invoice(
            meal_subscription_invoice_id=meal_subscription_invoice_id,
            stripe_payment_intent_id=stripe_payment_intent_id,
            stripe_invoice_id=stripe_invoice_id,
        )
