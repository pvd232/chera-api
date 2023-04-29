from service.Order_Meal_Service import Order_Meal_Service
from domain.Extended_Order_Meal_Domain import Extended_Order_Meal_Domain
from uuid import UUID
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from models import Order_Meal_Model


class Extended_Order_Meal_Service(Order_Meal_Service):
    def get_extended_order_meals(
        self, meal_subscription_id: UUID
    ) -> Optional[list[Extended_Order_Meal_Domain]]:
        order_meal_models: Optional[
            list["Order_Meal_Model"]
        ] = self.order_meal_repository.get_order_meals(
            meal_subscription_id=meal_subscription_id
        )
        if order_meal_models != None:
            order_meal_domains: list[Extended_Order_Meal_Domain] = [
                Extended_Order_Meal_Domain(order_meal_model=x)
                for x in order_meal_models
            ]
            return order_meal_domains
        else:
            return None
