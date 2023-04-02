from .Base_DTO import Base_DTO
from .Extended_Recipe_Ingredient_Nutrient_DTO import Extended_Recipe_Ingredient_Nutrient_DTO
from uuid import UUID


class Compressed_Nutrient_Data_DTO(Base_DTO):
    def __init__(self, extended_recipe_ingredient_nutrient_dto: Extended_Recipe_Ingredient_Nutrient_DTO) -> None:
        self.id: UUID = extended_recipe_ingredient_nutrient_dto.id
        self.recipe_ingredient_id: UUID = extended_recipe_ingredient_nutrient_dto.recipe_ingredient_id
        self.nutrient_id: str = extended_recipe_ingredient_nutrient_dto.nutrient_id
        self.usda_nutrient_daily_value_amount: float = extended_recipe_ingredient_nutrient_dto.usda_nutrient_daily_value_amount
        self.amount: float = extended_recipe_ingredient_nutrient_dto.amount
        self.nutrient_name: str = extended_recipe_ingredient_nutrient_dto.nutrient_name
        self.nutrient_unit: str = extended_recipe_ingredient_nutrient_dto.nutrient_unit
        self.usda_nutrient_id: str = extended_recipe_ingredient_nutrient_dto.usda_nutrient_id
