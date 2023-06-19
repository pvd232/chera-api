from .Base_DTO import Base_DTO
from typing import TYPE_CHECKING
from uuid import UUID

if TYPE_CHECKING:
    from domain.USDA_Ingredient_Portion_Domain import USDA_Ingredient_Portion_Domain


class USDA_Ingredient_Portion_DTO(Base_DTO):
    def __init__(
        self,
        usda_ingredient_portion_json: dict = None,
        usda_ingredient_portion_domain: "USDA_Ingredient_Portion_Domain" = None,
    ) -> None:
        if usda_ingredient_portion_json:
            self.id: UUID = UUID(usda_ingredient_portion_json["id"])
            self.usda_ingredient_id: str = usda_ingredient_portion_json[
                "usda_ingredient_id"
            ]
            self.fda_portion_id: str = str(
                usda_ingredient_portion_json["fda_portion_id"]
            )
            self.non_metric_unit: str = usda_ingredient_portion_json["non_metric_unit"]
            self.grams_per_non_metric_unit: float = float(
                usda_ingredient_portion_json["grams_per_non_metric_unit"]
            )
            self.portion_description: str = usda_ingredient_portion_json[
                "portion_description"
            ]
            self.is_imperial: bool = usda_ingredient_portion_json["is_imperial"]
            self.usda_data_type: str = usda_ingredient_portion_json["usda_data_type"]
            self.custom_value: bool = usda_ingredient_portion_json["custom_value"]
            self.multiplier: float = float(usda_ingredient_portion_json["multiplier"])
        elif usda_ingredient_portion_domain:
            self.id: UUID = usda_ingredient_portion_domain.id
            self.usda_ingredient_id: str = (
                usda_ingredient_portion_domain.usda_ingredient_id
            )
            self.fda_portion_id: str = usda_ingredient_portion_domain.fda_portion_id
            self.non_metric_unit: str = usda_ingredient_portion_domain.non_metric_unit
            self.grams_per_non_metric_unit: float = (
                usda_ingredient_portion_domain.grams_per_non_metric_unit
            )
            self.portion_description: str = (
                usda_ingredient_portion_domain.portion_description
            )
            self.is_imperial: bool = usda_ingredient_portion_domain.is_imperial
            self.usda_data_type: str = usda_ingredient_portion_domain.usda_data_type
            self.custom_value: bool = usda_ingredient_portion_domain.custom_value
            self.multiplier: float = usda_ingredient_portion_domain.multiplier
