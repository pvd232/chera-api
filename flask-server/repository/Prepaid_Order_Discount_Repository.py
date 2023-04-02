from repository.Base_Repository import Base_Repository
from models import Prepaid_Order_Discount_Model
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from domain.Prepaid_Order_Discount_Domain import Prepaid_Order_Discount_Domain


class Prepaid_Order_Discount_Repository(Base_Repository):
    def create_prepaid_order_discount(self, prepaid_order_discount_domain: 'Prepaid_Order_Discount_Domain') -> None:
        new_prepaid_order_discount = Prepaid_Order_Discount_Model(
            prepaid_order_discount_domain=prepaid_order_discount_domain)
        self.db.session.add(new_prepaid_order_discount)
        self.db.session.commit()
