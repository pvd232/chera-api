from .Scheduled_Order_Snack_Domain import Scheduled_Order_Snack_Domain
from .Snack_Domain import Snack_Domain
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models import Scheduled_Order_Snack_Model


class Extended_Scheduled_Order_Snack_Domain(Scheduled_Order_Snack_Domain):
    def __init__(
        self, scheduled_order_snack_model: "Scheduled_Order_Snack_Model"
    ) -> None:
        super().__init__(
            scheduled_order_snack_object=scheduled_order_snack_model,
            schedule_snack_object=None,
            scheduled_order_snack_id=None,
            delivery_date=None,
            is_paused=None,
        )
        self.associated_snack = Snack_Domain(
            snack_model=scheduled_order_snack_model.associated_snack
        )
