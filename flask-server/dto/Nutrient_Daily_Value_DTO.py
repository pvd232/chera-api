from .Base_DTO import Base_DTO
from uuid import UUID
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .Compressed_Nutrient_Data_DTO import Compressed_Nutrient_Data_DTO


class Nutrient_Daily_Value_DTO(Base_DTO):
    def __init__(
        self,
        compressed_nutrient_data_dto: "Compressed_Nutrient_Data_DTO",
        daily_value_amount: float,
    ):
        self.id = compressed_nutrient_data_dto.id
        self.name = compressed_nutrient_data_dto.nutrient_name
        self.nutrient_id = compressed_nutrient_data_dto.nutrient_id
        self.unit = compressed_nutrient_data_dto.nutrient_unit
        self.amount = compressed_nutrient_data_dto.amount
        self.daily_value_amount = daily_value_amount
