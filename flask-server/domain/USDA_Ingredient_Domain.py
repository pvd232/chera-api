from .Base_Domain import Base_Domain
from models import USDA_Ingredient_Model
from dto.USDA_Ingredient_DTO import USDA_Ingredient_DTO


class USDA_Ingredient_Domain(Base_Domain):
    def __init__(
        self, usda_ingredient_object: USDA_Ingredient_Model | USDA_Ingredient_DTO
    ) -> None:
        self.id: str = usda_ingredient_object.id
        self.name: str = usda_ingredient_object.name
        self.fdc_id: str = usda_ingredient_object.fdc_id
        self.amount_of_grams: float = usda_ingredient_object.amount_of_grams
        self.k_cal: int = usda_ingredient_object.k_cal
        self.k_cal_to_gram_ratio: float = usda_ingredient_object.k_cal_to_gram_ratio
        self.usda_data_type: str = usda_ingredient_object.usda_data_type
        self.fda_identifier: str = usda_ingredient_object.fda_identifier
        self.active: bool = usda_ingredient_object.active
