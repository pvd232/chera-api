from models import Scheduled_Order_Snack_Model
from .Base_Domain import Base_Domain
from .Schedule_Snack_Domain import Schedule_Snack_Domain
from dto.Scheduled_Order_Snack_DTO import Scheduled_Order_Snack_DTO
from datetime import date, datetime
from uuid import UUID
from typing import Optional


class Scheduled_Order_Snack_Domain(Base_Domain):
    def __init__(
        self,
        scheduled_order_snack_object: Optional[
            Scheduled_Order_Snack_Model | Scheduled_Order_Snack_DTO
        ],
        schedule_snack_object: Optional[Schedule_Snack_Domain],
        scheduled_order_snack_id: Optional[UUID],
        delivery_date: Optional[datetime],
        is_paused: Optional[bool],
    ) -> None:
        if scheduled_order_snack_object:
            self.id: UUID = scheduled_order_snack_object.id
            self.meal_subscription_id: UUID = (
                scheduled_order_snack_object.meal_subscription_id
            )
            self.snack_id: UUID = scheduled_order_snack_object.snack_id
            self.delivery_date: float = scheduled_order_snack_object.delivery_date
            self.delivery_skipped = scheduled_order_snack_object.delivery_skipped
            self.delivery_paused = scheduled_order_snack_object.delivery_paused
            self.datetime: float = scheduled_order_snack_object.datetime
        elif schedule_snack_object:
            self.id = scheduled_order_snack_id
            self.meal_subscription_id = schedule_snack_object.meal_subscription_id
            self.snack_id = schedule_snack_object.snack_id
            self.delivery_date: float = delivery_date
            self.delivery_skipped = False
            self.delivery_paused = is_paused
            self.datetime: float = scheduled_order_snack_object.datetime
