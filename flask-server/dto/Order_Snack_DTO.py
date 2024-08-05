from dto.Base_DTO import Base_DTO
from uuid import UUID
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from domain.Order_Snack_Domain import Order_Snack_Domain


class Order_Snack_DTO(Base_DTO):
    def __init__(
        self,
        order_snack_json: Optional[dict] = None,
        order_snack_domain: "Order_Snack_Domain" = None,
    ) -> None:
        if order_snack_json:
            self.id: UUID = UUID(order_snack_json["id"])
            self.scheduled_order_snack_id: UUID = UUID(
                order_snack_json["scheduled_order_snack_id"]
            )
            self.meal_subscription_invoice_id: UUID = UUID(
                order_snack_json["meal_subscription_invoice_id"]
            )
        elif order_snack_domain:
            self.id: UUID = order_snack_domain.id
            self.scheduled_order_snack_id: UUID = (
                order_snack_domain.scheduled_order_snack_id
            )
            self.meal_subscription_invoice_id: UUID = (
                order_snack_domain.meal_subscription_invoice_id
            )
