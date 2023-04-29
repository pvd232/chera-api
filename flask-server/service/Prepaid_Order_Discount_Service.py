from domain.Prepaid_Order_Discount_Domain import Prepaid_Order_Discount_Domain
from uuid import UUID
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from repository.Prepaid_Order_Discount_Repository import (
        Prepaid_Order_Discount_Repository,
    )


class Prepaid_Order_Discount_Service(object):
    def __init__(
        self, prepaid_order_discount_repository: "Prepaid_Order_Discount_Repository"
    ) -> None:
        self.prepaid_order_discount_repository = prepaid_order_discount_repository

    def create_prepaid_order_discount(
        self,
        discount_id: UUID,
        dietitian_prepayment_id: UUID,
        discount_percentage: float,
        num_meals: int,
        num_snacks: int,
        meal_price: float,
        snack_price: float,
    ) -> None:
        new_prepaid_order_discount_domain = Prepaid_Order_Discount_Domain(
            discount_id=discount_id,
            dietitian_prepayment_id=dietitian_prepayment_id,
            discount_percentage=discount_percentage,
            num_meals=num_meals,
            num_snacks=num_snacks,
            meal_price=meal_price,
            snack_price=snack_price,
        )
        self.prepaid_order_discount_repository.create_prepaid_order_discount(
            prepaid_order_discount_domain=new_prepaid_order_discount_domain
        )
