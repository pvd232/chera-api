from .Scheduled_Order_Snack_Service import Scheduled_Order_Snack_Service
from domain.Extended_Scheduled_Order_Snack_Domain import (
    Extended_Scheduled_Order_Snack_Domain,
)
from typing import Optional, TYPE_CHECKING
from uuid import UUID

if TYPE_CHECKING:
    from models import Scheduled_Order_Snack_Model


class Extended_Scheduled_Order_Snack_Service(Scheduled_Order_Snack_Service):
    def get_upcoming_extended_scheduled_order_snacks(
        self, meal_subscription_id: Optional[UUID] = None
    ) -> Optional[list["Extended_Scheduled_Order_Snack_Domain"]]:
        scheduled_order_snacks: Optional[list["Scheduled_Order_Snack_Model"]] = (
            self.scheduled_order_snack_repository.get_upcoming_scheduled_order_snacks(
                meal_subscription_id=meal_subscription_id
            )
        )
        if scheduled_order_snacks:
            return [
                Extended_Scheduled_Order_Snack_Domain(scheduled_order_snack_model=x)
                for x in scheduled_order_snacks
            ]
        else:
            return None
