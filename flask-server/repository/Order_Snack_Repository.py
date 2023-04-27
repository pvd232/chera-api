from repository.Base_Repository import Base_Repository
from models import Order_Snack_Model, Meal_Subscription_Invoice_Model
from datetime import datetime
from uuid import UUID
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from domain.Order_Snack_Domain import Order_Snack_Domain


class Order_Snack_Repository(Base_Repository):
    def create_order_snack(self, order_snack_domain: "Order_Snack_Domain") -> None:
        new_order_snack = Order_Snack_Model(order_snack=order_snack_domain)
        self.db.session.add(new_order_snack)
        self.db.session.commit()
        return

    def create_order_snacks(
        self, order_snack_domains: list["Order_Snack_Domain"]
    ) -> None:
        for order_snack in order_snack_domains:
            new_order_snack = Order_Snack_Model(order_snack=order_snack)
            self.db.session.add(new_order_snack)
        self.db.session.commit()
        return

    def get_order_snacks(
        self, meal_subscription_id: UUID
    ) -> Optional[list[Order_Snack_Model]]:
        order_snacks_to_return: list[Order_Snack_Model] = []
        meal_subscription_invoices: Optional[
            list[Meal_Subscription_Invoice_Model]
        ] = self.db.session.query(Meal_Subscription_Invoice_Model).filter(
            Meal_Subscription_Invoice_Model.meal_subscription_id == meal_subscription_id
        )
        if meal_subscription_invoices:
            for meal_subscription_invoice in meal_subscription_invoices:
                for order_snack in meal_subscription_invoice.order_snacks:
                    order_snacks_to_return.append(order_snack)
            return order_snacks_to_return
        else:
            return None
