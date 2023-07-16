from .Base_DTO import Base_DTO
from uuid import UUID


class Nutrient_Daily_Value_DTO(Base_DTO):
    def __init__(
        self,
        nutrient_id: str,
        daily_value: float,
        nutrient_unit: str,
    ):
        self.nutrient_id = nutrient_id
        self.daily_value = daily_value
        self.nutrient_unit = nutrient_unit
