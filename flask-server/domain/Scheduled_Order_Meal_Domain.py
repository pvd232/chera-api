from models import Scheduled_Order_Meal_Model
from .Base_Domain import Base_Domain
from .Schedule_Meal_Domain import Schedule_Meal_Domain
from dto.Scheduled_Order_Meal_DTO import Scheduled_Order_Meal_DTO
from datetime import date, datetime
from uuid import UUID
from typing import Optional


class Scheduled_Order_Meal_Domain(Base_Domain):
    def __init__(self, scheduled_order_meal_object: Optional[Scheduled_Order_Meal_Model | Scheduled_Order_Meal_DTO], schedule_meal_object: Optional[Schedule_Meal_Domain], scheduled_order_meal_id: Optional[UUID], delivery_date: Optional[datetime], is_paused: Optional[bool]) -> None:
        if scheduled_order_meal_object:
            self.id:UUID = scheduled_order_meal_object.id
            self.meal_subscription_id:UUID = scheduled_order_meal_object.meal_subscription_id
            self.meal_id:UUID = scheduled_order_meal_object.meal_id
            self.delivery_date:float = scheduled_order_meal_object.delivery_date
            self.delivery_skipped = scheduled_order_meal_object.delivery_skipped
            self.delivery_paused = scheduled_order_meal_object.delivery_paused
            self.datetime:float = scheduled_order_meal_object.datetime
        elif schedule_meal_object:
            self.id = scheduled_order_meal_id
            self.meal_subscription_id = schedule_meal_object.meal_subscription_id
            self.meal_id = schedule_meal_object.meal_id
            self.delivery_date:float = delivery_date
            self.delivery_skipped = False
            self.delivery_paused = is_paused
            self.datetime:float = scheduled_order_meal_object.datetime
