from uuid import UUID
from typing import TYPE_CHECKING, Optional
from .Base_DTO import Base_DTO

if TYPE_CHECKING:
    from domain.Snack_Domain import Snack_Domain


class Snack_DTO(Base_DTO):
    def __init__(
        self, snack_json: Optional[dict] = None, snack_domain: "Snack_Domain" = None
    ) -> None:
        if snack_json:
            self.id: UUID = UUID(snack_json["id"])
            self.name: str = snack_json["name"]
            self.description: str = snack_json["description"]
            self.image_url: str = snack_json["image_url"]
            self.active: bool = snack_json["active"]

        elif snack_domain:
            self.id: UUID = snack_domain.id
            self.name: str = snack_domain.name
            self.description: str = snack_domain.description
            self.image_url: str = snack_domain.image_url
            self.active: bool = snack_domain.active
