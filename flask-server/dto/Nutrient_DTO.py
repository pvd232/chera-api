from .Base_DTO import Base_DTO

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from domain.Nutrient_Domain import Nutrient_Domain


class Nutrient_DTO(Base_DTO):
    def __init__(self, nutrient_json: dict = None, nutrient_domain: 'Nutrient_Domain' = None) -> None:
        if nutrient_json:
            self.id: str = nutrient_json["id"]
            self.name: str = nutrient_json["name"]
            self.unit: str = nutrient_json["unit"]
            self.usda_id: str = nutrient_json["usda_id"]
            self.has_daily_value: bool = nutrient_json["has_daily_value"]
        elif nutrient_domain:
            self.id: str = nutrient_domain.id
            self.name: str = nutrient_domain.name
            self.unit: str = nutrient_domain.unit
            self.usda_id: str = nutrient_domain.usda_id
            self.has_daily_value: bool = nutrient_domain.has_daily_value
