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
        stripe_invoice_id: str,
        stripe_payment_intent_id: str,
    ) -> None:
        first_meal_subscription_invoice = (
            self.db.session.query(Meal_Subscription_Invoice_Model)
            .filter(Meal_Subscription_Invoice_Model.id == meal_subscription_invoice_id)
            .first()
        )
        first_meal_subscription_invoice.stripe_invoice_id = stripe_invoice_id
        first_meal_subscription_invoice.stripe_payment_intent_id = (
            stripe_payment_intent_id
        )
        self.db.session.commit()
