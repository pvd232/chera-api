from typing import TYPE_CHECKING
from dto.Nutrient_Daily_Value_DTO import Nutrient_Daily_Value_DTO

if TYPE_CHECKING:
    from dto.Extended_Meal_Plan_Meal_DTO import Extended_Meal_Plan_Meal_DTO
    from dto.Extended_Meal_Plan_Snack_DTO import Extended_Meal_Plan_Snack_DTO
    from dto.Snack_Nutrient_Stats_DTO import Snack_Nutrient_Stats_DTO
    from dto.Meal_Nutrient_Stats_DTO import Meal_Nutrient_Stats_DTO


class Food_Nutrient_Stats_Service:
    def extract_nutrient_stats(
        self,
        extended_meal_plan_food: "Extended_Meal_Plan_Meal_DTO"
        | "Extended_Meal_Plan_Snack_DTO",
    ) -> Meal_Nutrient_Stats_DTO | Snack_Nutrient_Stats_DTO:
        nutrient_list = []
        for nutrient in extended_meal_plan_food.nutrients.values():
            nutrient_daily_value_dto = Nutrient_Daily_Value_DTO(
                nutrient_id=nutrient.nutrient_id,
                usda_nutrient_daily_value_amount=nutrient.amount
                / nutrient.usda_nutrient_daily_value_amount,
                nutrient_unit=nutrient.nutrient_unit,
            )
            nutrient_list.append(nutrient_daily_value_dto)
        recipe_list = [x.usda_ingredient_name for x in extended_meal_plan_food.recipe]
        total_grams = 0
        for recipe in extended_meal_plan_food.recipe:
            total_grams += recipe.amount_of_grams

        serialized_food = extended_meal_plan_food.serialize()
        if hasattr(extended_meal_plan_food, "meal_time"):
            return Meal_Nutrient_Stats_DTO(
                meal_plan_id=extended_meal_plan_food.associated_meal_plan.id,
                recipe=recipe_list,
                nutrients=nutrient_list,
                recipe=recipe_list,
                k_cal=serialized_food["k_cal"],
                protein_k_cal=serialized_food["protein_k_cal"],
                fat_k_cal=serialized_food["fat_k_cal"],
                carb_k_cal=serialized_food["carb_k_cal"],
                weight=total_grams,
                associated_meal=extended_meal_plan_food.associated_meal,
            )
        else:
            return Snack_Nutrient_Stats_DTO(
                meal_plan_id=extended_meal_plan_food.associated_meal_plan.id,
                recipe=recipe_list,
                nutrients=nutrient_list,
                k_cal=serialized_food["k_cal"],
                protein_k_cal=serialized_food["protein_k_cal"],
                fat_k_cal=serialized_food["fat_k_cal"],
                carb_k_cal=serialized_food["carb_k_cal"],
                weight=total_grams,
                associated_snack=extended_meal_plan_food.associated_snack,
            )
