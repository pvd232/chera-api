from domain.Order_Meal_Domain import Order_Meal_Domain
from uuid import UUID
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from repository.Order_Meal_Repository import Order_Meal_Repository
    from dto.Order_Meal_DTO import Order_Meal_DTO


class Order_Meal_Service(object):
    def __init__(self, order_meal_repository: 'Order_Meal_Repository') -> None:
        self.order_meal_repository = order_meal_repository

    def create_order_meal(self, order_meal_domain: Order_Meal_Domain) -> None:
        self.order_meal_repository.create_order_meal(
            order_meal_domain=order_meal_domain)

    def create_order_meals(self, order_meal_dtos: list['Order_Meal_DTO']) -> None:
        order_meal_domains: list[Order_Meal_Domain] = [Order_Meal_Domain(
            order_meal_object=x) for x in order_meal_dtos]
        self.order_meal_repository.create_order_meals(
            order_meal_domains=order_meal_domains)

    def get_order_meals(self, meal_subscription_id: UUID) -> Optional[list[Order_Meal_Domain]]:
        order_meal_objects: Optional[list['Order_Meal_Domain']] = self.order_meal_repository.get_order_meals(
            meal_subscription_id=meal_subscription_id)
        if order_meal_objects:
            order_meal_domains: list[Order_Meal_Domain] = [
                Order_Meal_Domain(order_meal_object=x) for x in order_meal_objects]
            return order_meal_domains
        else:
            return None
