from repository.Base_Repository import Base_Repository
from models import Meal_Subscription_Invoice_Model, Meal_Model, Snack_Model
from uuid import UUID
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from repository.Meal_Subscription_Repository import Meal_Subscription_Repository
    from repository.Meal_Repository import Meal_Repository
    from repository.Snack_Repository import Snack_Repository
    from repository.Client_Repository import Client_Repository
    from repository.State_Sales_Tax_Repository import State_Sales_Tax_Repository
    from domain.Meal_Subscription_Invoice_Domain import Meal_Subscription_Invoice_Domain


class Meal_Subscription_Invoice_Repository(Base_Repository):
    def get_upcoming_meal_subscription_invoices(
        self, delivery_date: float
    ) -> list[Meal_Subscription_Invoice_Model]:
        upcoming_meal_subscription_invoices = (
            self.db.session.query(Meal_Subscription_Invoice_Model)
            .filter(Meal_Subscription_Invoice_Model.delivery_date == delivery_date)
            .all()
        )

        return upcoming_meal_subscription_invoices

    def get_meal_subscription_invoice(
        self,
        meal_subscription_invoice_id: UUID = None,
        stripe_payment_intent_id: str = None,
    ) -> Optional[Meal_Subscription_Invoice_Model]:
        if meal_subscription_invoice_id:
            meal_subscription_invoice = (
                self.db.session.query(Meal_Subscription_Invoice_Model)
                .filter(
                    Meal_Subscription_Invoice_Model.id == meal_subscription_invoice_id
                )
                .first()
            )
        elif stripe_payment_intent_id:
            meal_subscription_invoice = (
                self.db.session.query(Meal_Subscription_Invoice_Model)
                .filter(
                    Meal_Subscription_Invoice_Model.stripe_payment_intent_id
                    == stripe_payment_intent_id
                )
                .first()
            )
        return meal_subscription_invoice

    def get_meal_subscription_invoices(
        self, meal_subscription_id: UUID
    ) -> Optional[list[Meal_Subscription_Invoice_Model]]:
        meal_subscription_invoices: Optional[list[Meal_Subscription_Invoice_Model]] = (
            self.db.session.query(Meal_Subscription_Invoice_Model)
            .filter(
                Meal_Subscription_Invoice_Model.meal_subscription_id
                == meal_subscription_id
            )
            .all()
        )
        if meal_subscription_invoices:
            return meal_subscription_invoices
        else:
            return False

    def create_meal_subscription_invoice(
        self, meal_subscription_invoice_domain: "Meal_Subscription_Invoice_Domain"
    ) -> Meal_Subscription_Invoice_Model:
        new_subscription_invoice = Meal_Subscription_Invoice_Model(
            meal_subscription_invoice_domain=meal_subscription_invoice_domain
        )
        self.db.session.add(new_subscription_invoice)
        self.db.session.commit()
        return new_subscription_invoice

    def update_first_meal_subscription_invoice(
        self,
        meal_subscription_invoice_id: UUID,
        stripe_payment_intent_id: str,
        stripe_invoice_id: str,
        shipping_cost: float,
        meal_repository: "Meal_Repository",
        snack_repository: "Snack_Repository",
        meal_subscription_repository: "Meal_Subscription_Repository",
        client_repository: "Client_Repository",
        state_sales_tax_repository: "State_Sales_Tax_Repository",
    ) -> None:
        meal_subscription_invoice_to_update = (
            self.db.session.query(Meal_Subscription_Invoice_Model)
            .filter(Meal_Subscription_Invoice_Model.id == meal_subscription_invoice_id)
            .first()
        )

        meal_subscription_invoice_to_update.stripe_payment_intent_id = (
            stripe_payment_intent_id
        )
        meal_subscription_invoice_to_update.stripe_invoice_id = stripe_invoice_id
        service_fee = 0.0
        sales_tax_total = 0.0
        meals_subtotal = 0.0
        snacks_subtotal = 0.0
        total = 0.0

        for order_meal in meal_subscription_invoice_to_update.order_meals:
            meal: Meal_Model = meal_repository.get_meal(meal_id=order_meal.meal_id)
            meals_subtotal += meal.price

        for order_snack in meal_subscription_invoice_to_update.order_snacks:
            snack: Snack_Model = snack_repository.get_snack(
                snack_id=order_snack.snack_id
            )
            snacks_subtotal += snack.price

        meal_subscription = meal_subscription_repository.get_meal_subscription(
            meal_subscription_id=meal_subscription_invoice_to_update.meal_subscription_id
        )

        client = client_repository.get_client(client_id=meal_subscription.client_id)

        # TODO - make shipping cost dynamic based on distance
        meal_subscription_invoice_to_update.shipping_total = shipping_cost

        sales_tax_percentage = state_sales_tax_repository.get_sales_tax(
            state=client.state
        ).sales_tax_percentage

        sales_tax_total = sales_tax_percentage * (meals_subtotal + snacks_subtotal)
        pre_service_fee_total = meals_subtotal + snacks_subtotal + sales_tax_total + shipping_cost
        total = (pre_service_fee_total + 0.3) / (1 - 0.029)

        service_fee = total - pre_service_fee_total
        

        meal_subscription_invoice_to_update.total = total
        meal_subscription_invoice_to_update.subtotal = meals_subtotal
        meal_subscription_invoice_to_update.sales_tax_total = sales_tax_total
        meal_subscription_invoice_to_update.stripe_fee_total = service_fee
        meal_subscription_invoice_to_update.sales_tax_percentage = sales_tax_percentage
        self.db.session.commit()
        return
