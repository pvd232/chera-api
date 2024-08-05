from .Base_DTO import Base_DTO
from typing import TYPE_CHECKING, Optional
from uuid import UUID

if TYPE_CHECKING:
    from domain.Discount_Domain import Discount_Domain


class Discount_DTO(Base_DTO):
    def __init__(
        self,
        discount_json: Optional[dict] = None,
        discount_domain: "Discount_Domain" = None,
    ) -> None:
        if discount_json:
            self.id: UUID = discount_json["id"]
            self.code: str = discount_json["code"]
            self.discount_percentage: float = discount_json["discount_percentage"]
            self.active: bool = discount_json["active"]
        elif discount_domain:
            self.id: UUID = discount_domain.id
            self.code: str = discount_domain.code
            self.discount_percentage: float = discount_domain.discount_percentage
            self.active: bool = discount_domain.active
