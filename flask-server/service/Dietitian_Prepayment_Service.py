from domain.Dietitian_Prepayment_Domain import Dietitian_Prepayment_Domain
from dto.Dietitian_Prepayment_DTO import Dietitian_Prepayment_DTO
from datetime import datetime, timezone
from uuid import uuid4 as uuid
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from repository.Dietitian_Prepayment_Repository import (
        Dietitian_Prepayment_Repository,
    )
    from service.Discount_Service import Discount_Service
    from service.Prepaid_Order_Discount_Service import Prepaid_Order_Discount_Service
    from domain.Discount_Domain import Discount_Domain


class Dietitian_Prepayment_Service(object):
    def __init__(
        self, dietitian_prepayment_repository: "Dietitian_Prepayment_Repository"
    ) -> None:
        self.dietitian_prepayment_repository = dietitian_prepayment_repository

    def set_prepayment_values(
        self,
        num_meals: int,
        num_snacks: int,
        dietitian_prepayment_domain: Dietitian_Prepayment_Domain,
        meal_price: float,
        snack_price: float,
        shipping_cost: float,
        discount_percentage: float = None,
    ) -> Dietitian_Prepayment_Domain:
        service_fee = 0.0
        sales_tax_total = 0.0
        meals_subtotal = meal_price * float(num_meals)
        snacks_subtotal = snack_price * float(num_snacks)
        if discount_percentage:
            meals_subtotal = meals_subtotal * discount_percentage
            snacks_subtotal = snacks_subtotal * discount_percentage
        total = 0.0

        # no sales tax until 500K revenue
        sales_tax_percentage = 0
        sales_tax_total = 0
        total = meals_subtotal + sales_tax_total + snacks_subtotal + shipping_cost
        service_fee = (0.029 * total) + 0.3

        dietitian_prepayment_domain.total = total
        dietitian_prepayment_domain.subtotal = meals_subtotal
        dietitian_prepayment_domain.sales_tax_total = sales_tax_total
        dietitian_prepayment_domain.stripe_fee_total = service_fee
        dietitian_prepayment_domain.sales_tax_percentage = sales_tax_percentage
        dietitian_prepayment_domain.shipping_total = shipping_cost
        dietitian_prepayment_domain.datetime = datetime.now(timezone.utc).timestamp()
        return dietitian_prepayment_domain

    def create_dietitian_prepayment(
        self,
        num_meals: int,
        num_snacks: int,
        discount_code: str,
        dietitian_id: str,
        staged_client_id: str,
        stripe_payment_intent_id: str,
        meal_price: float,
        snack_price: float,
        shipping_cost: float,
        discount_service: "Discount_Service",
        prepaid_order_discount_service: "Prepaid_Order_Discount_Service",
    ) -> None:
        discount: Optional["Discount_Domain"] = discount_service.verify_discount_code(
            discount_code=discount_code
        )
        if discount:
            discount_percentage = discount.discount_percentage
        else:
            discount_percentage = None
        dietitian_prepayment_dto = Dietitian_Prepayment_DTO(
            dietitian_prepayment_json={
                "id": uuid(),
                "dietitian_id": dietitian_id,
                "staged_client_id": staged_client_id,
                "subtotal": 0.0,
                "sales_tax_percentage": 0.0,
                "sales_tax_total": 0.0,
                "shipping_total": 0.0,
                "stripe_fee_total": 0.0,
                "stripe_payment_intent_id": stripe_payment_intent_id,
                "total": 0.0,
                "datetime": "",
            }
        )
        pre_update_new_dietitian_prepayment_domain = Dietitian_Prepayment_Domain(
            dietitian_prepayment_object=dietitian_prepayment_dto
        )

        pre_update_new_dietitian_prepayment_domain.id = uuid()
        pre_update_new_dietitian_prepayment_domain.dietitian_id = dietitian_id
        pre_update_new_dietitian_prepayment_domain.staged_client_id = staged_client_id
        pre_update_new_dietitian_prepayment_domain.stripe_payment_intent_id = (
            stripe_payment_intent_id
        )

        post_update_new_dietitian_prepayment_domain = self.set_prepayment_values(
            num_meals=num_meals,
            num_snacks=num_snacks,
            dietitian_prepayment_domain=pre_update_new_dietitian_prepayment_domain,
            discount_percentage=discount_percentage,
            meal_price=meal_price,
            snack_price=snack_price,
            shipping_cost=shipping_cost,
        )

        self.dietitian_prepayment_repository.create_dietitian_prepayment(
            dietiitan_prepayment_domain=post_update_new_dietitian_prepayment_domain
        )

        if discount:
            prepaid_order_discount_service.create_prepaid_order_discount(
                discount_id=discount.id,
                dietitian_prepayment_id=post_update_new_dietitian_prepayment_domain.id,
                discount_percentage=discount.discount_percentage,
                num_meals=num_meals,
                num_snacks=num_snacks,
                meal_price=meal_price,
                snack_price=snack_price,
            )
        return
