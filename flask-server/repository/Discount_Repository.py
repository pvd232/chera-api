from repository.Base_Repository import Base_Repository
from models import Discount_Model
from typing import Optional


class Discount_Repository(Base_Repository):
    def get_discount(self, discount_code: str) -> Discount_Model:
        requested_discount = (
            self.db.session.query(Discount_Model)
            .filter(Discount_Model.code == discount_code)
            .first()
        )
        return requested_discount

    def verify_discount(self, discount_code: str) -> Optional[Discount_Model]:
        requested_discount = (
            self.db.session.query(Discount_Model)
            .filter(Discount_Model.code == discount_code)
            .first()
        )
        if requested_discount:
            return requested_discount
        else:
            return None
