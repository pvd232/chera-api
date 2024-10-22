from dto.Base_DTO import Base_DTO
from uuid import UUID
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from domain.USDA_Nutrient_Daily_Value_Domain import USDA_Nutrient_Daily_Value_Domain


class USDA_Nutrient_Daily_Value_DTO(Base_DTO):
    def __init__(
        self,
        usda_nutrient_daily_value_json: Optional[dict] = None,
        usda_nutrient_daily_value_domain: "USDA_Nutrient_Daily_Value_Domain" = None,
    ) -> None:
        if usda_nutrient_daily_value_json:
            self.id: UUID = usda_nutrient_daily_value_json["id"]
            self.nutrient_id: str = usda_nutrient_daily_value_json["nutrient_id"]
            self.meal_plan_id: UUID = usda_nutrient_daily_value_json["meal_plan_id"]
            self.amount: float = usda_nutrient_daily_value_json["amount"]
            self.unit: str = usda_nutrient_daily_value_json["unit"]

        elif usda_nutrient_daily_value_domain:
            self.id: UUID = usda_nutrient_daily_value_domain.id
            self.nutrient_id: str = usda_nutrient_daily_value_domain.nutrient_id
            self.meal_plan_id: UUID = usda_nutrient_daily_value_domain.meal_plan_id
            self.amount: float = usda_nutrient_daily_value_domain.amount
            self.unit: str = usda_nutrient_daily_value_domain.unit
