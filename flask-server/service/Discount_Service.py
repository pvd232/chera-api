from domain.Discount_Domain import Discount_Domain
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from repository.Discount_Repository import Discount_Repository


class Discount_Service(object):
    def __init__(self, discount_repository: 'Discount_Repository') -> None:
        self.discount_repository = discount_repository

    def verify_discount_code(self, discount_code: str) -> Optional[Discount_Domain]:
        discount_code = self.discount_repository.verify_discount(
            discount_code=discount_code)
        if discount_code:
            return Discount_Domain(discount_object=discount_code)
        else:
            return None
