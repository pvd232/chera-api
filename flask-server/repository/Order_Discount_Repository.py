from repository.Base_Repository import Base_Repository
from models import Order_Discount_Model
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from domain.Order_Discount_Domain import Order_Discount_Domain


class Order_Discount_Repository(Base_Repository):
    def create_order_discount(self,  order_discount_domain: 'Order_Discount_Domain') -> None:
        new_order_discount = Order_Discount_Model(
            order_discount_domain=order_discount_domain)
        self.db.session.add(new_order_discount)
        self.db.session.commit()
