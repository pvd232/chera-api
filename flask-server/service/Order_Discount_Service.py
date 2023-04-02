from domain.Order_Discount_Domain import Order_Discount_Domain
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from repository.Order_Discount_Repository import Order_Discount_Repository
    from dto.Order_Discount_DTO import Order_Discount_DTO


class Order_Discount_Service(object):
    def __init__(self, order_discount_repository: 'Order_Discount_Repository') -> None:
        self.order_discount_repository = order_discount_repository

    def create_order_discount(self, order_discount_dto: 'Order_Discount_DTO') -> None:
        new_order_discount_domain = Order_Discount_Domain(
            order_discount_object=order_discount_dto)
        self.order_discount_repository.create_order_discount(
            order_discount_domain=new_order_discount_domain)
