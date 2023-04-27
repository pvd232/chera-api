from .Meal_Plan_Snack_DTO import Meal_Plan_Snack_DTO
from .Extended_Recipe_Ingredient_DTO import Extended_Recipe_Ingredient_DTO
from .Snack_DTO import Snack_DTO
from .Extended_Meal_Plan_DTO import Extended_Meal_Plan_DTO
from .Compressed_Nutrient_Data_DTO import Compressed_Nutrient_Data_DTO
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from domain.Extended_Meal_Plan_Snack_Domain import Extended_Meal_Plan_Snack_Domain


class Extended_Meal_Plan_Snack_DTO(Meal_Plan_Snack_DTO):
    def __init__(
        self, extended_meal_plan_snack_domain: "Extended_Meal_Plan_Snack_Domain"
    ) -> None:
        super().__init__(meal_plan_snack_domain=extended_meal_plan_snack_domain)
        self.recipe: list[Extended_Recipe_Ingredient_DTO] = [
            Extended_Recipe_Ingredient_DTO(extended_recipe_ingredient_domain=x)
            for x in extended_meal_plan_snack_domain.recipe
        ]
        self.associated_snack = Snack_DTO(
            snack_domain=extended_meal_plan_snack_domain.associated_snack
        )
        self.associated_snack_plan = Extended_Meal_Plan_DTO(
            extended_meal_plan_domain=extended_meal_plan_snack_domain.associated_meal_plan
        )

        self.nutrients: dict[str, Compressed_Nutrient_Data_DTO] = {}
        for recipe_ingredient in self.recipe:
            for nutrient in recipe_ingredient.nutrients:
                if nutrient.nutrient_id in self.nutrients:
                    self.nutrients[nutrient.nutrient_id].amount += nutrient.amount
                else:
                    self.nutrients[nutrient.nutrient_id] = Compressed_Nutrient_Data_DTO(
                        extended_recipe_ingredient_nutrient_dto=nutrient
                    )

    def get_k_cal(self) -> float:
        sum = 0
        for ingredient in self.recipe:
            sum += ingredient.k_cal
        return sum

    def get_protein_k_cal(self) -> float:
        return self.nutrients["protein"].amount * 4.0

    def get_fat_k_cal(self) -> float:
        return self.nutrients["fat"].amount * 9.0

    def get_carb_k_cal(self) -> float:
        return self.nutrients["carb"].amount * 4.0

    def get_nutritional_k_cal_adjustment(self) -> None:
        suggested_k_cal = self.get_k_cal()
        nutritional_k_cal = (
            self.get_fat_k_cal() + self.get_carb_k_cal() + self.get_protein_k_cal()
        )
        return suggested_k_cal / nutritional_k_cal

    def get_adjusted_protein_k_cal(self) -> float:
        return self.get_protein_k_cal() * self.get_nutritional_k_cal_adjustment()

    def get_adjusted_fat_k_cal(self) -> float:
        return self.get_fat_k_cal() * self.get_nutritional_k_cal_adjustment()

    def get_adjusted_carb_k_cal(self) -> float:
        return self.get_carb_k_cal() * self.get_nutritional_k_cal_adjustment()

    def serialize(self) -> dict:
        attribute_names = list(self.__dict__.keys())
        attributes = list(self.__dict__.values())
        serialized_attributes = super().serialize()
        for i in range(len(attributes)):
            if attribute_names[i] == "recipe":
                serialized_attributes[attribute_names[i]] = [
                    x.serialize() for x in attributes[i]
                ]
            elif attribute_names[i] == "nutrients":
                serialized_attributes[attribute_names[i]] = [
                    x.serialize() for x in attributes[i].values()
                ]
        serialized_attributes["k_cal"] = round(self.get_k_cal())
        serialized_attributes["protein_k_cal"] = round(
            self.get_adjusted_protein_k_cal()
        )
        serialized_attributes["fat_k_cal"] = round(self.get_adjusted_fat_k_cal())
        serialized_attributes["carb_k_cal"] = round(self.get_adjusted_carb_k_cal())
        return serialized_attributes
