from .Base_Domain import Base_Domain
from models import USDA_Ingredient_Portion_Model
from dto.USDA_Ingredient_Portion_DTO import USDA_Ingredient_Portion_DTO


class USDA_Ingredient_Portion_Domain(Base_Domain):
    def __init__(self,  usda_ingredient_portion_object: USDA_Ingredient_Portion_Model | USDA_Ingredient_Portion_DTO) -> None:
        self.id = usda_ingredient_portion_object.id
        self.usda_ingredient_id = usda_ingredient_portion_object.usda_ingredient_id
        self.fda_portion_id = usda_ingredient_portion_object.fda_portion_id
        self.non_metric_unit = usda_ingredient_portion_object.non_metric_unit
        self.grams_per_non_metric_unit = usda_ingredient_portion_object.grams_per_non_metric_unit
        self.portion_description = usda_ingredient_portion_object.portion_description
        self.is_imperial = usda_ingredient_portion_object.is_imperial
        self.usda_data_type = usda_ingredient_portion_object.usda_data_type
        self.custom_value = usda_ingredient_portion_object.custom_value
