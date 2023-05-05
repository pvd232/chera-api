from uuid import UUID
from datetime import datetime
from typing import TYPE_CHECKING
from .Base_DTO import Base_DTO

if TYPE_CHECKING:
    from domain.Scheduled_Order_Meal_Domain import Scheduled_Order_Meal_Domain


class Scheduled_Order_Meal_DTO(Base_DTO):
    def __init__(
        self,
        scheduled_order_meal_json: dict = None,
        scheduled_order_meal_domain: "Scheduled_Order_Meal_Domain" = None,
    ) -> None:
        if scheduled_order_meal_json:
            self.id: UUID = UUID(scheduled_order_meal_json["id"])
            self.meal_subscription_id: UUID = UUID(
                scheduled_order_meal_json["meal_subscription_id"]
            )
            self.meal_id: UUID = UUID(scheduled_order_meal_json["meal_id"])
            self.delivery_date: float = float(
                scheduled_order_meal_json["delivery_date"]
            )
            self.delivery_skipped: bool = scheduled_order_meal_json["delivery_skipped"]
            self.delivery_paused: bool = scheduled_order_meal_json["delivery_paused"]
            self.datetime: float = float(scheduled_order_meal_json["datetime"])
        elif scheduled_order_meal_domain:
            self.id: UUID = scheduled_order_meal_domain.id
            self.meal_subscription_id: UUID = (
                scheduled_order_meal_domain.meal_subscription_id
            )
            self.meal_id: UUID = scheduled_order_meal_domain.meal_id
            self.delivery_date: float = scheduled_order_meal_domain.delivery_date
            self.delivery_skipped: bool = scheduled_order_meal_domain.delivery_skipped
            self.delivery_paused: bool = scheduled_order_meal_domain.delivery_paused
            self.datetime: float = scheduled_order_meal_domain.datetime
