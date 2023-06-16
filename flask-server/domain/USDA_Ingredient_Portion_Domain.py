from .Base_Domain import Base_Domain
from models import USDA_Ingredient_Portion_Model
from dto.USDA_Ingredient_Portion_DTO import USDA_Ingredient_Portion_DTO
from uuid import UUID


class USDA_Ingredient_Portion_Domain(Base_Domain):
    def __init__(
        self,
        usda_ingredient_portion_object: USDA_Ingredient_Portion_Model
        | USDA_Ingredient_Portion_DTO,
    ) -> None:
        self.id: UUID = usda_ingredient_portion_object.id
        self.usda_ingredient_id: str = usda_ingredient_portion_object.usda_ingredient_id
        self.fda_portion_id: str = usda_ingredient_portion_object.fda_portion_id
        self.non_metric_unit: str = usda_ingredient_portion_object.non_metric_unit
        self.grams_per_non_metric_unit: float = (
            usda_ingredient_portion_object.grams_per_non_metric_unit
        )
        self.portion_description: str = (
            usda_ingredient_portion_object.portion_description
        )
        self.is_imperial: bool = usda_ingredient_portion_object.is_imperial
        self.usda_data_type: str = usda_ingredient_portion_object.usda_data_type
        self.custom_value: bool = usda_ingredient_portion_object.custom_value
        self.multiplier: float = usda_ingredient_portion_object.multiplier
