from models import Nutrient_Model
from .Base_Domain import Base_Domain
from dto.Nutrient_DTO import Nutrient_DTO


class Nutrient_Domain(Base_Domain):
    def __init__(self, nutrient_object: Nutrient_Model | Nutrient_DTO) -> None:
        if nutrient_object:
            self.id = nutrient_object.id
            self.name = nutrient_object.name
            self.unit = nutrient_object.unit
            self.usda_id = nutrient_object.usda_id
            self.has_daily_value = nutrient_object.has_daily_value
