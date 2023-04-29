from domain.Meal_Subscription_Invoice_Domain import Meal_Subscription_Invoice_Domain
from uuid import UUID
from typing import Optional, TYPE_CHECKING
from datetime import datetime, date

if TYPE_CHECKING:
    from models import Meal_Subscription_Invoice_Model
    from repository.Meal_Subscription_Invoice_Repository import (
        Meal_Subscription_Invoice_Repository,
    )
    from repository.Meal_Subscription_Repository import Meal_Subscription_Repository
    from repository.Client_Repository import Client_Repository
    from repository.Meal_Repository import Meal_Repository
    from repository.State_Sales_Tax_Repository import State_Sales_Tax_Repository
    from service.Scheduled_Order_Meal_Service import Scheduled_Order_Meal_Service
    from service.Meal_Service import Meal_Service
    from service.Snack_Service import Snack_Service
    from service.Scheduled_Order_Meal_Service import Scheduled_Order_Meal_Service
    from service.Scheduled_Order_Snack_Service import Scheduled_Order_Snack_Service
    from domain.Meal_Subscription_Domain import Meal_Subscription_Domain
    from domain.Meal_Domain import Meal_Domain
    from domain.Snack_Domain import Snack_Domain
    from domain.Scheduled_Order_Meal_Domain import Scheduled_Order_Meal_Domain
    from domain.Scheduled_Order_Snack_Domain import Scheduled_Order_Snack_Domain
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
        meal_subscription_invoice_id: UUID = None,
        stripe_payment_intent_id: str = None,
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
            first_created_meal_subscription_invoice: Meal_Subscription_Invoice_Domain = meal_subscription_invoices[
                -1
            ]
            return first_created_meal_subscription_invoice
        else:
            return None

    # CONFIRMED OUTPUTING CORRECT VALUES, MATCHING STRIPE
    def set_meal_subscription_invoice_total(
        self,
        meal_subscription_invoice: Meal_Subscription_Invoice_Domain,
        scheduled_order_meal_domains: list["Scheduled_Order_Meal_Domain"],
        scheduled_order_snack_domains: list["Scheduled_Order_Snack_Domain"],
        shipping_cost: float,
        meal_service: "Meal_Service",
        snack_service: "Snack_Service",
    ) -> Meal_Subscription_Invoice_Domain:
        service_fee: float = 0.0
        sales_tax_total: float = 0.0
        meals_subtotal: float = 0.0
        snacks_subtotal: float = 0.0
        total: float = 0.0

        for scheduled_order_meal_domain in scheduled_order_meal_domains:
            meal: "Meal_Domain" = meal_service.get_meal(
                scheduled_order_meal_domain.meal_id
            )
            meals_subtotal += meal.price

        for scheduled_order_snack_domain in scheduled_order_snack_domains:
            snack: "Snack_Domain" = snack_service.get_snack(
                scheduled_order_snack_domain.snack_id
            )
            snacks_subtotal += snack.price

        meal_subscription_invoice.shipping_total = shipping_cost

        # No sales tax until 500K revenue
        sales_tax_percentage = 0
        sales_tax_total = 0
        pre_service_fee_total = (
            meals_subtotal + snacks_subtotal + sales_tax_total + shipping_cost
        )

        # https://support.stripe.com/questions/passing-the-stripe-fee-on-to-customers
        total = (pre_service_fee_total + 0.3) / (1 - 0.029)

        meal_subscription_invoice.total = total
        meal_subscription_invoice.subtotal = meals_subtotal
        meal_subscription_invoice.sales_tax_total = sales_tax_total
        meal_subscription_invoice.stripe_fee_total = service_fee
        meal_subscription_invoice.sales_tax_percentage = sales_tax_percentage
        meal_subscription_invoice.shipping_total = 0
        return meal_subscription_invoice

    def create_meal_subscription_invoice(
        self,
        meal_subscription_invoice_dto: "Meal_Subscription_Invoice_DTO",
        shipping_cost: float,
        scheduled_order_meal_service: "Scheduled_Order_Meal_Service",
        scheduled_order_snack_service: "Scheduled_Order_Snack_Service",
        meal_service: "Meal_Service",
        snack_service: "Snack_Service",
    ) -> Meal_Subscription_Invoice_Domain:
        pre_cost_meal_subscription_invoice: Meal_Subscription_Invoice_Domain = (
            Meal_Subscription_Invoice_Domain(
                meal_subscription_invoice_object=meal_subscription_invoice_dto
            )
        )

        associated_scheduled_order_meals = scheduled_order_meal_service.get_scheduled_order_meals_for_week(
            meal_subscription_id=pre_cost_meal_subscription_invoice.meal_subscription_id,
            delivery_date=pre_cost_meal_subscription_invoice.delivery_date,
        )

        associated_scheduled_order_snacks = scheduled_order_snack_service.get_scheduled_order_snacks_for_week(
            meal_subscription_id=pre_cost_meal_subscription_invoice.meal_subscription_id,
            delivery_date=pre_cost_meal_subscription_invoice.delivery_date,
        )

        post_cost_meal_subscription_invoice: Meal_Subscription_Invoice_Domain = (
            self.set_meal_subscription_invoice_total(
                meal_subscription_invoice=pre_cost_meal_subscription_invoice,
                scheduled_order_meal_domains=associated_scheduled_order_meals,
                scheduled_order_snack_domains=associated_scheduled_order_snacks,
                shipping_cost=shipping_cost,
                meal_service=meal_service,
                snack_service=snack_service,
            )
        )

        created_meal_subscription_invoice: "Meal_Subscription_Invoice_Model" = (
            self.meal_subscription_invoice_repository.create_meal_subscription_invoice(
                meal_subscription_invoice_domain=post_cost_meal_subscription_invoice
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
        shipping_cost: float,
        scheduled_order_meal_service: "Scheduled_Order_Meal_Service",
        scheduled_order_snack_service: "Scheduled_Order_Snack_Service",
        meal_service: "Meal_Service",
        snack_service: "Snack_Service",
    ) -> Meal_Subscription_Invoice_Domain:
        new_meal_subscription_invoice_domain = Meal_Subscription_Invoice_Domain(
            meal_subscription_invoice_object=meal_subscription_invoice_dto
        )
        new_meal_subscription_invoice_domain.meal_subscription_id = meal_subscription.id
        new_meal_subscription_invoice_domain.stripe_invoice_id = stripe_invoice_id
        new_meal_subscription_invoice_domain.stripe_payment_intent_id = (
            stripe_payment_intent_id
        )

        service_fee: float = 0.0
        sales_tax_total: float = 0.0
        meals_subtotal: float = 0.0
        snacks_subtotal: float = 0.0
        total: float = 0.0

        scheduled_order_meals: list[
            "Scheduled_Order_Meal_Domain"
        ] = scheduled_order_meal_service.get_scheduled_order_meals_for_week(
            meal_subscription_id=meal
        )
        for scheduled_order_meal in scheduled_order_meals:
            meal: "Meal_Domain" = meal_service.get_meal(
                meal_id=scheduled_order_meal.meal_id
            )
            meals_subtotal += meal.price

        scheduled_order_snacks: list[
            "Scheduled_Order_Snack_Domain"
        ] = scheduled_order_snack_service.get_scheduled_order_snacks_for_week(
            meal_subscription_id=meal
        )
        for scheduled_order_snack in scheduled_order_snacks:
            snack: "Snack_Domain" = snack_service.get_snack(
                snack_id=scheduled_order_snack.snack_id
            )
            snacks_subtotal += snack.price

        sales_tax_percentage = 0.0
        sales_tax_total = sales_tax_percentage * meals_subtotal

        total = meals_subtotal + snacks_subtotal + sales_tax_total

        service_fee = (0.029 * total) + 0.3

        new_meal_subscription_invoice_domain.total = round(total, 2)
        new_meal_subscription_invoice_domain.subtotal = round(meals_subtotal, 2)
        new_meal_subscription_invoice_domain.sales_tax_total = round(sales_tax_total, 2)
        new_meal_subscription_invoice_domain.stripe_fee_total = round(service_fee, 2)
        new_meal_subscription_invoice_domain.sales_tax_percentage = sales_tax_percentage
        new_meal_subscription_invoice_domain.shipping_total = shipping_cost

        created_invoice = (
            self.meal_subscription_invoice_repository.create_meal_subscription_invoice(
                meal_subscription_invoice_domain=new_meal_subscription_invoice_domain
            )
        )
        created_invoice_domain = Meal_Subscription_Invoice_Domain(
            meal_subscription_invoice_object=created_invoice
        )
        return created_invoice_domain

    def update_first_meal_subscription_invoice(
        self,
        meal_subscription_invoice_id: UUID,
        stripe_payment_intent_id: str,
        stripe_invoice_id: str,
        shipping_cost: float,
        meal_repository: "Meal_Repository",
        meal_subscription_repository: "Meal_Subscription_Repository",
        client_repository: "Client_Repository",
        state_sales_tax_repository: "State_Sales_Tax_Repository",
    ) -> None:
        self.meal_subscription_invoice_repository.update_first_meal_subscription_invoice(
            meal_subscription_invoice_id=meal_subscription_invoice_id,
            stripe_payment_intent_id=stripe_payment_intent_id,
            stripe_invoice_id=stripe_invoice_id,
            shipping_cost=shipping_cost,
            meal_repository=meal_repository,
            meal_subscription_repository=meal_subscription_repository,
            client_repository=client_repository,
            state_sales_tax_repository=state_sales_tax_repository,
        )
