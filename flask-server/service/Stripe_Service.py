import stripe
from datetime import datetime
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from service.Order_Calc_Service import Order_Calc_Service
    from service.Date_Service import Date_Service
    from domain.Discount_Domain import Discount_Domain


class Stripe_Service(object):
    def create_payment_intent(
        self,
        number_of_meals: int,
        number_of_snacks: int,
        meal_price: float,
        snack_price: float,
        shipping_cost: float,
        order_calc_service: "Order_Calc_Service" = None,
        discount_percentage: float = False,
    ) -> dict:
        stripe_order_total = order_calc_service.get_stripe_order_total(
            num_meals=number_of_meals,
            num_snacks=number_of_snacks,
            meal_price=meal_price,
            snack_price=snack_price,
            shipping_cost=shipping_cost,
            discount_percentage=discount_percentage,
        )

        intent = stripe.PaymentIntent.create(
            amount=stripe_order_total,
            currency="usd",
            automatic_payment_methods={
                "enabled": True,
            },
        )
        return {
            "client_secret": intent["client_secret"],
            "stripe_payment_intent_id": intent["id"],
        }

    def get_payment_intent(self, stripe_payment_intent_id: str) -> stripe.PaymentIntent:
        return stripe.PaymentIntent.retrieve(stripe_payment_intent_id)

    def get_invoice(self, invoice_id: str) -> stripe.Invoice:
        invoice = stripe.Invoice.retrieve(invoice_id)
        return invoice

    def create_stripe_customer(self, client_id: str) -> stripe.Customer:
        return stripe.Customer.create(email=client_id)

    def get_subscription(self, stripe_subscription_id: str) -> stripe.Subscription:
        return stripe.Subscription.retrieve(stripe_subscription_id)

    def create_stripe_subscription(
        self,
        number_of_meals: int,
        number_of_snacks: int,
        client_id: str,
        stripe_meal_price_id: str,
        stripe_one_time_meal_price_id: str,
        stripe_one_time_fnce_discounted_meal_price_id: str,
        stripe_snack_price_id: str,
        stripe_one_time_snack_price_id: str,
        stripe_one_time_fnce_discounted_snack_price_id: str,
        stripe_shipping_price_id: str,
        stripe_one_time_shipping_price_id: str,
        stripe_one_time_account_setup_fee: float,
        date_service: "Date_Service",
        discount: "Discount_Domain" = None,
        prepaid=False,
    ) -> dict:
        trial_end = int(date_service.get_stripe_delivery_date_anchor())
        if discount:
            stripe_meal_one_time_price_id_to_use = (
                stripe_one_time_fnce_discounted_meal_price_id
            )
            stripe_snack_one_time_price_id_to_use = (
                stripe_one_time_fnce_discounted_snack_price_id
            )
        else:
            stripe_meal_one_time_price_id_to_use = stripe_one_time_meal_price_id
            stripe_snack_one_time_price_id_to_use = stripe_one_time_snack_price_id

        stripe_customer: stripe.Customer = self.create_stripe_customer(
            client_id=client_id
        )

        # Current week will be paid for and invoiced immidiately, subsequent invoice will be upcoming wednesday, the billing anchor, and will be discounted 100% to account for up front payment of first week
        if not prepaid:
            subscription = stripe.Subscription.create(
                customer=stripe_customer.id,
                items=[
                    {
                        "price": stripe_meal_price_id,
                        "quantity": number_of_meals,
                    },
                    {
                        "price": stripe_snack_price_id,
                        "quantity": number_of_snacks,
                    },
                    {"price": stripe_shipping_price_id, "quantity": 1},
                ],
                payment_behavior="default_incomplete",
                expand=["latest_invoice.payment_intent"],
                trial_end=trial_end,
                add_invoice_items=[
                    {
                        "price": stripe_meal_one_time_price_id_to_use,
                        "quantity": number_of_meals,
                    },
                    {
                        "price": stripe_snack_one_time_price_id_to_use,
                        "quantity": number_of_snacks,
                    },
                    {"price": stripe_one_time_shipping_price_id, "quantity": 1},
                ],
            )

        # Remove add_invoice_items to prevent immidiate charge on the account, thus the first week is free
        else:
            subscription: stripe.Subscription = stripe.Subscription.create(
                customer=stripe_customer.id,
                items=[
                    {
                        "price": stripe_meal_price_id,
                        "quantity": number_of_meals,
                    },
                    {
                        "price": stripe_snack_price_id,
                        "quantity": number_of_snacks,
                    },
                    {"price": stripe_shipping_price_id, "quantity": 1},
                ],
                payment_behavior="default_incomplete",
                expand=["latest_invoice.payment_intent"],
                trial_end=trial_end,
                add_invoice_items=[
                    {"price": stripe_one_time_account_setup_fee, "quantity": 1}
                ],
            )
        return {
            "stripe_subscription_id": subscription.id,
            "client_secret": subscription.latest_invoice.payment_intent.client_secret,
            "client_stripe_id": subscription.customer,
        }

    def update_subscription(
        self,
        stripe_subscription_id: str,
        number_of_meals: int,
        number_of_snacks: int,
        stripe_meal_price_id: str,
        stripe_snack_price_id: str,
    ) -> None:
        subscription: stripe.Subscription = stripe.Subscription.retrieve(
            stripe_subscription_id
        )

        # Meal subscription item is first item in list, snack subscription item is second item in list, shipping subscription item is third item in list
        stripe.Subscription.modify(
            stripe_subscription_id,
            cancel_at_period_end=False,
            proration_behavior="create_prorations",
            items=[
                {
                    "id": subscription["items"]["data"][0].id,
                    "price": stripe_meal_price_id,
                    "quantity": number_of_meals,
                },
                {
                    "id": subscription["items"]["data"][1].id,
                    "price": stripe_snack_price_id,
                    "quantity": number_of_snacks,
                },
            ],
        )
        return

    def delete_subscription(self, stripe_subscription_id: str) -> None:
        old_subscription = stripe.Subscription.retrieve(stripe_subscription_id)
        if old_subscription:
            stripe.Subscription.delete(stripe_subscription_id)
        return

    def pause_stripe_subscription(self, stripe_subscription_id: str) -> None:
        stripe.Subscription.modify(
            stripe_subscription_id, pause_collection={"behavior": "void"}
        )
        return

    def unpause_stripe_subscription(self, stripe_subscription_id: str) -> None:
        stripe.Subscription.modify(stripe_subscription_id, pause_collection="")
        return

    def apply_coupon(self, stripe_subscription_id: str) -> None:
        stripe.Subscription.modify(
            stripe_subscription_id,
            coupon=stripe.Coupon.create(duration="once", percent_off=100),
        )
        return

    def skip_week(
        self,
        stripe_subscription_id: str,
        delivery_date: datetime,
        date_service: "Date_Service",
    ) -> None:
        datetime_to_resume = int(
            date_service.get_next_week_delivery_date(
                current_delivery_date=delivery_date
            )
        )
        stripe.Subscription.modify(
            stripe_subscription_id,
            pause_collection={
                "behavior": "keep_as_draft",
                "resumes_at": datetime_to_resume,
            },
        )
        return

    def unskip_week(self, stripe_subscription_id: str) -> None:
        stripe.Subscription.modify(
            stripe_subscription_id,
            pause_collection="",
        )
        return
