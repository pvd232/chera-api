from models import Order_Snack_Model
from .Base_Domain import Base_Domain
from dto.Order_Snack_DTO import Order_Snack_DTO
from uuid import UUID


class Order_Snack_Domain(Base_Domain):
    def __init__(self, order_snack_object: Order_Snack_Model | Order_Snack_DTO) -> None:
        self.id: UUID = order_snack_object.id
        self.meal_subscription_invoice_id: UUID = (
            order_snack_object.meal_subscription_invoice_id
        )
        self.scheduled_order_snack_id: UUID = (
            order_snack_object.scheduled_order_snack_id
        )
