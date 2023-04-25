from uuid import UUID
from typing import TYPE_CHECKING
from .Base_DTO import Base_DTO

if TYPE_CHECKING:
    from domain.Scheduled_Order_Snack_Domain import Scheduled_Order_Snack_Domain


class Scheduled_Order_Snack_DTO(Base_DTO):
    def __init__(
        self,
        scheduled_order_snack_json: dict = None,
        scheduled_order_snack_domain: "Scheduled_Order_Snack_Domain" = None,
    ) -> None:
        if scheduled_order_snack_json:
            self.id: UUID = UUID(scheduled_order_snack_json["id"])
            self.meal_subscription_id: UUID = UUID(
                scheduled_order_snack_json["meal_subscription_id"]
            )
            self.snack_id: str = scheduled_order_snack_json["snack_id"]
            self.delivery_date: float = float(
                scheduled_order_snack_json["delivery_date"]
            )
            self.delivery_skipped: bool = scheduled_order_snack_json["delivery_skipped"]
            self.delivery_paused: bool = scheduled_order_snack_json["delivery_paused"]
            self.datetime: float = float(scheduled_order_snack_json["datetime"])
        elif scheduled_order_snack_domain:
            self.id: UUID = scheduled_order_snack_domain.id
            self.meal_subscription_id: UUID = (
                scheduled_order_snack_domain.meal_subscription_id
            )
            self.snack_id: str = scheduled_order_snack_domain.snack_id
            self.delivery_date: float = scheduled_order_snack_domain.delivery_date
            self.delivery_skipped: bool = scheduled_order_snack_domain.delivery_skipped
            self.delivery_paused: bool = scheduled_order_snack_domain.delivery_paused
            self.datetime: float = scheduled_order_snack_domain.datetime
