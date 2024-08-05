from typing import TYPE_CHECKING, Optional
from .Base_DTO import Base_DTO

if TYPE_CHECKING:
    from domain.COGS_Domain import COGS_Domain


class COGS_DTO(Base_DTO):
    def __init__(
        self, cogs_json: Optional[dict] = None, cogs_domain: "COGS_Domain" = None
    ) -> None:
        if cogs_json:
            self.num_meals: int = cogs_json["num_meals"]
            self.is_local: bool = cogs_json["is_local"]
            self.ingredient: float = cogs_json["ingredient"]
            self.core_packaging: float = cogs_json["core_packaging"]
            self.kitchen: float = cogs_json["kitchen"]
            self.chef: float = cogs_json["chef"]
            self.box: float = cogs_json["box"]
            self.ice: float = cogs_json["ice"]
            self.num_boxes: int = cogs_json["num_boxes"]

        elif cogs_domain:
            self.num_meals: int = cogs_domain.num_meals
            self.is_local: bool = cogs_domain.is_local
            self.ingredient: float = cogs_domain.ingredient
            self.core_packaging: float = cogs_domain.core_packaging
            self.kitchen: float = cogs_domain.kitchen
            self.chef: float = cogs_domain.chef
            self.box: float = cogs_domain.box
            self.ice: float = cogs_domain.ice
            self.num_boxes: int = cogs_domain.num_boxes
