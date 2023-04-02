from .Order_Meal_Domain import Order_Meal_Domain
from .Extended_Scheduled_Order_Meal_Email_Summary_Domain import Extended_Scheduled_Order_Meal_Email_Summary_Domain
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models import Order_Meal_Model


class Extended_Order_Meal_Domain(Order_Meal_Domain):
    def __init__(self, order_meal_model: 'Order_Meal_Model') -> None:
        super().__init__(order_meal_object=order_meal_model)

        self.scheduled_order_meal = Extended_Scheduled_Order_Meal_Email_Summary_Domain(
            scheduled_order_meal_object=order_meal_model.scheduled_order_meal)
