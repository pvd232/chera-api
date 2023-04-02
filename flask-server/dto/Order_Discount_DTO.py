from .Base_DTO import Base_DTO
from uuid import UUID
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from domain.Order_Discount_Domain import Order_Discount_Domain


class Order_Discount_DTO(Base_DTO):
    def __init__(self, order_discount_json: dict, order_discount_domain: 'Order_Discount_Domain') -> None:
        if order_discount_json:
            self.discount_id: UUID = UUID(order_discount_json["discount_id"])
            self.staged_client_id: str = order_discount_json["staged_client_id"]
            self.amount: float = float(order_discount_json["amount"])
            self.datetime: float = float(order_discount_json["datetime"])
        elif order_discount_domain:
            self.discount_id: UUID = order_discount_domain.discount_id
            self.staged_client_id: str = order_discount_domain.staged_client_id
            self.amount: float = order_discount_domain.amount
            self.datetime: float = order_discount_domain.datetime
