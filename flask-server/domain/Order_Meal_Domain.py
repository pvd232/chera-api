from models import Order_Meal_Model
from .Base_Domain import Base_Domain
from dto.Order_Meal_DTO import Order_Meal_DTO
from uuid import UUID


class Order_Meal_Domain(Base_Domain):
    def __init__(self, order_meal_object: Order_Meal_Model | Order_Meal_DTO) -> None:
        self.id: UUID = order_meal_object.id
        self.meal_subscription_invoice_id: UUID = order_meal_object.meal_subscription_invoice_id
        self.scheduled_order_meal_id: UUID = order_meal_object.scheduled_order_meal_id