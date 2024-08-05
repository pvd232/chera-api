from typing import TYPE_CHECKING, Optional
from .Base_DTO import Base_DTO
from uuid import UUID

if TYPE_CHECKING:
    from domain.Meal_Dietary_Restriction_Domain import Meal_Dietary_Restriction_Domain


class Meal_Dietary_Restriction_DTO(Base_DTO):
    def __init__(
        self,
        meal_dietary_restriction_json: Optional[dict] = None,
        meal_dietary_restriction_domain: "Meal_Dietary_Restriction_Domain" = None,
    ) -> None:
        if meal_dietary_restriction_json:
            self.id: UUID = UUID(meal_dietary_restriction_json["id"])
            self.meal_id: UUID = UUID(meal_dietary_restriction_json["meal_id"])
            self.dietary_restriction_id: str = meal_dietary_restriction_json[
                "dietary_restriction_id"
            ]

        elif meal_dietary_restriction_domain:
            self.id: UUID = meal_dietary_restriction_domain.id
            self.meal_id: UUID = meal_dietary_restriction_domain.meal_id
            self.dietary_restriction_id: str = (
                meal_dietary_restriction_domain.dietary_restriction_id
            )
