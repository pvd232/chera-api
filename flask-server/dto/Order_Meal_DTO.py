from dto.Base_DTO import Base_DTO
from uuid import UUID
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from domain.Order_Meal_Domain import Order_Meal_Domain


class Order_Meal_DTO(Base_DTO):
    def __init__(
        self,
        order_meal_json: Optional[dict] = None,
        order_meal_domain: "Order_Meal_Domain" = None,
    ) -> None:
        if order_meal_json:
            self.id: UUID = UUID(order_meal_json["id"])
            self.scheduled_order_meal_id: UUID = UUID(
                order_meal_json["scheduled_order_meal_id"]
            )
            self.meal_subscription_invoice_id: UUID = UUID(
                order_meal_json["meal_subscription_invoice_id"]
            )
        elif order_meal_domain:
            self.id: UUID = order_meal_domain.id
            self.scheduled_order_meal_id: UUID = (
                order_meal_domain.scheduled_order_meal_id
            )
            self.meal_subscription_invoice_id: UUID = (
                order_meal_domain.meal_subscription_invoice_id
            )
