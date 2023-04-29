from .Base_Domain import Base_Domain
from datetime import datetime, timezone
from uuid import UUID


class Prepaid_Order_Discount_Domain(Base_Domain):
    def __init__(
        self,
        discount_id: UUID,
        dietitian_prepayment_id: UUID,
        discount_percentage: float,
        num_meals: int,
        num_snacks: int,
        meal_price: float,
        snack_price: float,
    ) -> None:
        self.discount_id = discount_id
        self.dietitian_prepayment_id = dietitian_prepayment_id
        self.amount = (
            (num_meals * meal_price) + (num_snacks * snack_price)
        ) * discount_percentage
        self.datetime = datetime.now(timezone.utc)
