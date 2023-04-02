from .Scheduled_Order_Meal_Domain import Scheduled_Order_Meal_Domain
from .Extended_Meal_Email_Summary_Domain import Extended_Meal_Email_Summary_Domain
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models import Scheduled_Order_Meal_Model


class Extended_Scheduled_Order_Meal_Email_Summary_Domain(Scheduled_Order_Meal_Domain):
    def __init__(self, scheduled_order_meal_model: 'Scheduled_Order_Meal_Model') -> None:
        super().__init__(scheduled_order_meal_object=scheduled_order_meal_model,
                         schedule_meal_object=None, scheduled_order_meal_id=None, delivery_date=None, is_paused=None)
        self.associated_meal = Extended_Meal_Email_Summary_Domain(
            meal_object=scheduled_order_meal_model.associated_meal)
