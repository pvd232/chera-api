from .Meal_Subscription_Invoice_Domain import Meal_Subscription_Invoice_Domain
from domain.Extended_Order_Meal_Email_Summary_Domain import Extended_Scheduled_Order_Meal_Email_Summary_Domain
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models import Meal_Subscription_Invoice_Model


class Extended_Meal_Subscription_Invoice_Domain(Meal_Subscription_Invoice_Domain):
    def __init__(self, meal_subscription_invoice_model: 'Meal_Subscription_Invoice_Model') -> None:
        super().__init__(meal_subscription_invoice_object=meal_subscription_invoice_model)
        self.order_meals = [Extended_Scheduled_Order_Meal_Email_Summary_Domain(
            order_meal_object=x) for x in meal_subscription_invoice_model.order_meals]
