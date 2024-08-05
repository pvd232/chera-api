from dto.Base_DTO import Base_DTO
from uuid import UUID
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from domain.Meal_Sample_Domain import Meal_Sample_Domain


class Meal_Sample_DTO(Base_DTO):
    def __init__(
        self,
        meal_sample_json: Optional[dict] = None,
        meal_sample_domain: "Meal_Sample_Domain" = None,
    ) -> None:
        if meal_sample_json:
            self.id: UUID = meal_sample_json["id"]
            self.meal_id: UUID = meal_sample_json["meal_id"]
            self.dietitian_id: UUID = meal_sample_json["dietitian_id"]
        elif meal_sample_domain:
            self.id: UUID = meal_sample_domain.id
            self.meal_id: UUID = meal_sample_domain.meal_id
            self.dietitian_id: UUID = meal_sample_domain.dietitian_id
