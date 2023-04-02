from .Base_DTO import Base_DTO
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from domain.Discount_Domain import Discount_Domain


class Discount_DTO(Base_DTO):
    def __init__(self, discount_json: dict = None, discount_domain: 'Discount_Domain' = None) -> None:
        if discount_json:
            self.id = discount_json["id"]
            self.code = discount_json["code"]
            self.discount_percentage = discount_json["discount_percentage"]
            self.active = discount_json["active"]
        elif discount_domain:
            self.id = discount_domain.id
            self.code = discount_domain.code
            self.discount_percentage = discount_domain.discount_percentage
            self.active = discount_domain.active
