from service.Order_Snack_Service import Order_Snack_Service
from domain.Extended_Order_Snack_Domain import Extended_Order_Snack_Domain
from uuid import UUID
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from models import Order_Snack_Model


class Extended_Order_Snack_Service(Order_Snack_Service):
    def get_extended_order_snacks(
        self, meal_subscription_id: UUID
    ) -> Optional[list[Extended_Order_Snack_Domain]]:
        order_snack_models: Optional[
            list["Order_Snack_Model"]
        ] = self.order_snack_repository.get_order_snacks(
            meal_subscription_id=meal_subscription_id
        )
        if order_snack_models != None:
            order_snack_domains: list[Extended_Order_Snack_Domain] = [
                Extended_Order_Snack_Domain(order_snack_object=x)
                for x in order_snack_models
            ]
            return order_snack_domains
        else:
            return None
