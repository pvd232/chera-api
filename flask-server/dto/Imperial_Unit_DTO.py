from typing import TYPE_CHECKING
from .Base_DTO import Base_DTO

if TYPE_CHECKING:
    from domain.Imperial_Unit_Domain import Imperial_Unit_Domain


class Imperial_Unit_DTO(Base_DTO):
    def __init__(
        self,
        imperial_unit_json: dict = None,
        imperial_unit_domain: "Imperial_Unit_Domain" = None,
    ) -> None:
        if imperial_unit_json:
            self.id: str = imperial_unit_json["id"]
            self.ounces: float = imperial_unit_json["ounces"]

        elif imperial_unit_domain:
            self.id: str = imperial_unit_domain.id
            self.ounces: float = imperial_unit_domain.ounces
