from .Recipe_Ingredient_DTO import Recipe_Ingredient_DTO
from .Extended_Recipe_Ingredient_Nutrient_DTO import Extended_Recipe_Ingredient_Nutrient_DTO
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from domain.Extended_Recipe_Ingredient_Domain import Extended_Recipe_Ingredient_Domain


class Extended_Recipe_Ingredient_DTO(Recipe_Ingredient_DTO):
    def __init__(self, extended_recipe_ingredient_domain: 'Extended_Recipe_Ingredient_Domain') -> None:
        super().__init__(recipe_ingredient_domain=extended_recipe_ingredient_domain)
        self.nutrients: list[Extended_Recipe_Ingredient_Nutrient_DTO] = [Extended_Recipe_Ingredient_Nutrient_DTO(
            extended_recipe_ingredient_nutrient_domain=x) for x in extended_recipe_ingredient_domain.nutrients]
        self.usda_ingredient_name = extended_recipe_ingredient_domain.usda_ingredient.name
        self.usda_ingredient_fdc_id = extended_recipe_ingredient_domain.usda_ingredient.fdc_id
        self.fda_portion_id = extended_recipe_ingredient_domain.usda_ingredient_portion.fda_portion_id
        self.amount_of_grams = extended_recipe_ingredient_domain.usda_ingredient_portion.grams_per_non_metric_unit * self.quantity
        self.is_imperial = extended_recipe_ingredient_domain.usda_ingredient_portion.is_imperial
        self.non_metric_unit = extended_recipe_ingredient_domain.usda_ingredient_portion.non_metric_unit
        self.k_cal = self.amount_of_grams * \
            extended_recipe_ingredient_domain.usda_ingredient.k_cal_to_gram_ratio

    def serialize(self) -> dict:
        attribute_names = list(self.__dict__.keys())
        attributes = list(self.__dict__.values())
        serialized_attributes = super().serialize()
        for i in range(len(attributes)):
            if attribute_names[i] == "nutrients":
                serialized_attributes[attribute_names[i]] = [
                    x.serialize() for x in attributes[i]]
        return serialized_attributes
