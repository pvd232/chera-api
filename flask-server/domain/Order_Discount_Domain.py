from .Base_Domain import Base_Domain
from models import Order_Discount_Model
from dto.Order_Discount_DTO import Order_Discount_DTO
from uuid import UUID


class Order_Discount_Domain(Base_Domain):
    def __init__(self, order_discount_object: Order_Discount_Model | Order_Discount_DTO) -> None:
        self.discount_id: UUID = UUID(order_discount_object["discount_id"])
        self.staged_client_id: str = order_discount_object["staged_client_id"]
        self.amount: float = order_discount_object["amount"]
        self.datetime: float = float(order_discount_object["datetime"])
