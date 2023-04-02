from repository.Base_Repository import Base_Repository
from models import Order_Meal_Model, Meal_Subscription_Invoice_Model
from datetime import datetime
from uuid import UUID
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from domain.Order_Meal_Domain import Order_Meal_Domain


class Order_Meal_Repository(Base_Repository):
    def create_order_meal(self, order_meal_domain: 'Order_Meal_Domain') -> None:
        new_order_meal = Order_Meal_Model(order_meal=order_meal_domain)
        self.db.session.add(new_order_meal)
        self.db.session.commit()
        return

    def create_order_meals(self,  order_meal_domains: list['Order_Meal_Domain']) -> None:
        for order_meal in order_meal_domains:
            new_order_meal = Order_Meal_Model(order_meal=order_meal)
            self.db.session.add(new_order_meal)
        self.db.session.commit()
        return

    def get_order_meals(self,  meal_subscription_id: UUID) -> Optional[list[Order_Meal_Model]]:
        order_meals_to_return: list[Order_Meal_Model] = []
        meal_subscription_invoices: Optional[list[Meal_Subscription_Invoice_Model]] = self.db.session.query(
            Meal_Subscription_Invoice_Model).filter(Meal_Subscription_Invoice_Model.meal_subscription_id == meal_subscription_id)
        if meal_subscription_invoices:
            for meal_subscription_invoice in meal_subscription_invoices:
                for order_meal in meal_subscription_invoice.order_meals:
                    order_meals_to_return.append(order_meal)
            return order_meals_to_return
        else:
            return None
