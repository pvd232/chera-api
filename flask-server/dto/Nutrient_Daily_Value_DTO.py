from .Base_DTO import Base_DTO
from uuid import UUID


class Nutrient_Daily_Value_DTO(Base_DTO):
    def __init__(
        self,
        nutrient_id: str,
        usda_nutrient_daily_value_amount: float,
        nutrient_unit: str,
    ):
        self.nutrient_id = nutrient_id
        self.usda_nutrient_daily_value_amount = usda_nutrient_daily_value_amount
        self.nutrient_unit = nutrient_unit
