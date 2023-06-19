from .Base_DTO import Base_DTO
from uuid import UUID
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from domain.USDA_Ingredient_Nutrient_Domain import USDA_Ingredient_Nutrient_Domain


class USDA_Ingredient_Nutrient_DTO(Base_DTO):
    def __init__(
        self,
        usda_ingredient_nutrient_json: dict = None,
        usda_ingredient_nutrient_domain: "USDA_Ingredient_Nutrient_Domain" = None,
    ) -> None:
        if usda_ingredient_nutrient_json:
            self.id: UUID = usda_ingredient_nutrient_json["id"]
            self.usda_ingredient_id: str = usda_ingredient_nutrient_json[
                "usda_ingredient_id"
            ]
            self.nutrient_id: str = usda_ingredient_nutrient_json["nutrient_id"]
            self.amount: float = usda_ingredient_nutrient_json["amount"]
        elif usda_ingredient_nutrient_domain:
            self.id: UUID = UUID(usda_ingredient_nutrient_domain.id)
            self.usda_ingredient_id: str = (
                usda_ingredient_nutrient_domain.usda_ingredient_id
            )
            self.nutrient_id: str = usda_ingredient_nutrient_domain.nutrient_id
            self.amount: float = float(usda_ingredient_nutrient_domain.amount)
