from .Order_Snack_Domain import Order_Snack_Domain
from .Extended_Scheduled_Order_Snack_Domain import Extended_Scheduled_Order_Snack_Domain
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models import Order_Snack_Model


class Extended_Order_Snack_Domain(Order_Snack_Domain):
    def __init__(self, order_snack_model: "Order_Snack_Model") -> None:
        super().__init__(order_snack_object=order_snack_model)

        self.scheduled_order_snack = Extended_Scheduled_Order_Snack_Domain(
            scheduled_order_snack_object=order_snack_model.scheduled_order_snack
        )
