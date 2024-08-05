from .Base_DTO import Base_DTO
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from domain.Dietary_Restriction_Domain import Dietary_Restriction_Domain


class Dietary_Restriction_DTO(Base_DTO):
    def __init__(
        self,
        dietary_restriction_json: Optional[dict] = None,
        dietary_restriction_domain: "Dietary_Restriction_Domain" = None,
    ) -> None:
        if dietary_restriction_json:
            self.id = dietary_restriction_json["id"]
        elif dietary_restriction_domain:
            self.id = dietary_restriction_domain.id
