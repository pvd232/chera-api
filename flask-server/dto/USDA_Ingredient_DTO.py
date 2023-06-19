from .Base_DTO import Base_DTO
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from domain.USDA_Ingredient_Domain import USDA_Ingredient_Domain


class USDA_Ingredient_DTO(Base_DTO):
    def __init__(
        self,
        usda_ingredient_json: dict = None,
        usda_ingredient_domain: "USDA_Ingredient_Domain" = None,
    ) -> None:
        if usda_ingredient_json:
            self.id = usda_ingredient_json["id"]
            self.name = usda_ingredient_json["name"]
            self.fdc_id = usda_ingredient_json["fdc_id"]
            self.amount_of_grams = usda_ingredient_json["amount_of_grams"]
            self.k_cal = usda_ingredient_json["k_cal"]
            self.k_cal_to_gram_ratio = usda_ingredient_json["k_cal_to_gram_ratio"]
            self.usda_data_type = usda_ingredient_json["usda_data_type"]
            self.fda_identifier = usda_ingredient_json["fda_identifier"]
            self.active = usda_ingredient_json["active"]
        elif usda_ingredient_domain:
            self.id = usda_ingredient_domain.id
            self.name = usda_ingredient_domain.name
            self.fdc_id = usda_ingredient_domain.fdc_id
            self.amount_of_grams = usda_ingredient_domain.amount_of_grams
            self.k_cal = usda_ingredient_domain.k_cal
            self.k_cal_to_gram_ratio = usda_ingredient_domain.k_cal_to_gram_ratio
            self.usda_data_type = usda_ingredient_domain.usda_data_type
            self.fda_identifier = usda_ingredient_domain.fda_identifier
            self.active = usda_ingredient_domain.active
