import stripe
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from service.Order_Calc_Service import Order_Calc_Service
    from service.Date_Service import Date_Service
    from domain.Discount_Domain import Discount_Domain


class Stripe_Service(object):
    def create_payment_intent(
        self,
        num_items: int,
        meal_price: float,
        order_calc_service: "Order_Calc_Service" = None,
        discount_percentage: float = False,
    ) -> dict:
        stripe_order_total = order_calc_service.get_stripe_order_total(
            num_items=num_items,
            meal_price=meal_price,
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

    def get_price(self, meal_price: float, recurring: bool) -> dict:
        prices = stripe.Price.list(limit=100)
        for price in prices["data"]:
            if recurring:
                if (
                    round(price["unit_amount"]) == round(meal_price * 100)
                    and price["type"] == "recurring"
                ):  # Stripe uses cents
                    return {
                        "price_id": price["id"],
                        "amount": price["unit_amount"] / 100,
                    }
            else:
                if (
                    round(price["unit_amount"]) == round(meal_price * 100)
                    and price["type"] == "one_time"
                ):  # Stripe uses cents
                    return {
                        "price_id": price["id"],
                        "amount": price["unit_amount"] / 100,
                    }

    def get_payment_intent(self, stripe_payment_intent_id: str) -> stripe.PaymentIntent:
        return stripe.PaymentIntent.retrieve(stripe_payment_intent_id)

    def get_invoice(self, invoice_id: str) -> stripe.Invoice:
        invoice = stripe.Invoice.retrieve(invoice_id)
        return invoice

    def create_stripe_customer(self, client_email: str) -> stripe.Customer:
        return stripe.Customer.create(email=client_email)

    def delete_customer(self, customer_id: str) -> stripe.Customer:
        stripe_customer = stripe.Customer.retrieve(customer_id)
        if stripe_customer:
            stripe_customer.delete()
        return

    def get_payment_methods(self, stripe_customer_id: str):
        return stripe.PaymentMethod.list(customer=stripe_customer_id, type="card")

    def update_payment_method(
        self,
        stripe_customer_id: str,
        stripe_payment_method_id: str,
        stripe_subscription_id: str,
    ) -> None:
        try:
            stripe.PaymentMethod.attach(
                stripe_payment_method_id,
                customer=stripe_customer_id,
            )
            stripe.Customer.modify(
                stripe_customer_id,
                invoice_settings={"default_payment_method": stripe_payment_method_id},
            )
            stripe.Subscription.modify(
                stripe_subscription_id,
                default_payment_method=stripe_payment_method_id,
            )
            return True
        except stripe.error.StripeError as e:
            error_message = e.user_message or str(e)
            print("error_message", error_message)
            return False

    def get_subscription(self, stripe_subscription_id: str) -> stripe.Subscription:
        return stripe.Subscription.retrieve(stripe_subscription_id)

    def create_stripe_subscription(
        self,
        num_items: int,
        meal_price: int,
        client_email: str,
        stripe_one_time_account_setup_fee_price_id: str,
        date_service: "Date_Service",
        discount: "Discount_Domain" = None,
        prepaid=False,
    ) -> dict:
        trial_end = int(date_service.get_stripe_delivery_date_anchor())

        stripe_customer: stripe.Customer = self.create_stripe_customer(
            client_email=client_email
        )
        stripe_price = self.get_price(meal_price=meal_price, recurring=True)
        stripe_meal_one_time_price = self.get_price(
            meal_price=meal_price, recurring=False
        )

        # Current week will be paid for and invoiced immidiately, subsequent invoice will be upcoming wednesday, the billing anchor, and will be discounted 100% to account for up front payment of first week
        if not prepaid:
            if discount:
                subscription = stripe.Subscription.create(
                    customer=stripe_customer.id,
                    items=[
                        {
                            "price": stripe_price["price_id"],
                            "quantity": num_items,
                        },
                    ],
                    payment_behavior="default_incomplete",
                    expand=["latest_invoice.payment_intent"],
                    trial_end=trial_end,
                    add_invoice_items=[
                        {
                            "price": stripe_meal_one_time_price["price_id"],
                            "quantity": num_items,
                        }
                    ],
                    coupon=stripe.Coupon.create(
                        duration="once", percent_off=discount.discount_percentage * 100
                    ),
                )
            else:
                subscription = stripe.Subscription.create(
                    customer=stripe_customer.id,
                    items=[
                        {
                            "price": stripe_price["price_id"],
                            "quantity": num_items,
                        },
                    ],
                    payment_behavior="default_incomplete",
                    expand=["latest_invoice.payment_intent"],
                    trial_end=trial_end,
                    add_invoice_items=[
                        {
                            "price": stripe_meal_one_time_price["price_id"],
                            "quantity": num_items,
                        }
                    ],
                )

        # Remove add_invoice_items to prevent immidiate charge on the account, thus the first week is free
        else:
            subscription: stripe.Subscription = stripe.Subscription.create(
                customer=stripe_customer.id,
                items=[
                    {
                        "price": stripe_price["price_id"],
                        "quantity": num_items,
                    },
                ],
                payment_behavior="default_incomplete",
                expand=["latest_invoice.payment_intent"],
                trial_end=trial_end,
                add_invoice_items=[
                    {"price": stripe_one_time_account_setup_fee_price_id, "quantity": 1}
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
        num_items: int,
        stripe_meal_price_id: str,
    ) -> None:
        subscription: stripe.Subscription = stripe.Subscription.retrieve(
            stripe_subscription_id
        )

        # Meal subscription item is first item in list, snack subscription item is second item in list, shipping subscription item is third item in list
        stripe.Subscription.modify(
            stripe_subscription_id,
            cancel_at_period_end=False,
            proration_behavior="none",
            items=[
                {
                    "id": subscription["items"]["data"][0].id,
                    "price": stripe_meal_price_id,
                    "quantity": num_items,
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
            date_service.get_next_week_date(current_delivery_date=delivery_date)
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
