from domain.Order_Snack_Domain import Order_Snack_Domain
from uuid import UUID
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from repository.Order_Snack_Repository import Order_Snack_Repository
    from dto.Order_Snack_DTO import Order_Snack_DTO


class Order_Snack_Service(object):
    def __init__(self, order_snack_repository: "Order_Snack_Repository") -> None:
        self.order_snack_repository = order_snack_repository

    def create_order_snack(self, order_snack_domain: Order_Snack_Domain) -> None:
        self.order_snack_repository.create_order_snack(
            order_snack_domain=order_snack_domain
        )

    def create_order_snacks(self, order_snack_dtos: list["Order_Snack_DTO"]) -> None:
        order_snack_domains: list[Order_Snack_Domain] = [
            Order_Snack_Domain(order_snack_object=x) for x in order_snack_dtos
        ]
        self.order_snack_repository.create_order_snacks(
            order_snack_domains=order_snack_domains
        )

    def get_order_snacks(
        self, meal_subscription_id: UUID
    ) -> Optional[list[Order_Snack_Domain]]:
        order_snack_objects: Optional[
            list["Order_Snack_Domain"]
        ] = self.order_snack_repository.get_order_snacks(
            meal_subscription_id=meal_subscription_id
        )
        if order_snack_objects:
            order_snack_domains: list[Order_Snack_Domain] = [
                Order_Snack_Domain(order_snack_object=x) for x in order_snack_objects
            ]
            return order_snack_domains
        else:
            return None
