from typing import TYPE_CHECKING
from dto.Nutrient_Daily_Value_DTO import Nutrient_Daily_Value_DTO

if TYPE_CHECKING:
    from domain.Extended_Meal_Plan_Meal_Domain import Extended_Meal_Plan_Meal_Domain
    from domain.Extended_Meal_Plan_Snack_Domain import Extended_Meal_Plan_Snack_Domain
    from dto.Food_Nutrient_Stats_DTO import Food_Nutrient_Stats_DTO
    from dto.Meal_Nutrient_Stats_DTO import Meal_Nutrient_Stats_DTO


class Food_Nutrient_Stats_Service:
    def extract_nutrient_stats(
        self,
        extended_meal_plan_food: "Extended_Meal_Plan_Meal_Domain"
        | "Extended_Meal_Plan_Snack_Domain",
    ) -> Meal_Nutrient_Stats_DTO | Food_Nutrient_Stats_DTO:
        first_ingredient = extended_meal_plan_food.recipe[0]
        first_ingredient_nutrients = first_ingredient.nutrients
        nutrient_dict: dict[str : dict[str : float | str]] = {}
        for nutrient in first_ingredient_nutrients:
            if nutrient.id not in nutrient_dict:
                nutrient_dict[nutrient.id] = {
                    "nutrient_id": nutrient.id,
                    "nutrient_unit": nutrient.nutrient_unit,
                    "amount": nutrient.amount,
                    "usda_nutrient_daily_value_amount": nutrient.usda_nutrient_daily_value_amount,
                }

        # Skip first ingredient since its nutrients were already added
        for i in range(1, len(extended_meal_plan_food.recipe)):
            recipe_ingredient = extended_meal_plan_food.recipe[i]
            for nutrient in recipe_ingredient.nutrients:
                nutrient_dict[nutrient.id]["amount"] = nutrient.amount + nutrient_dict[
                    nutrient.id
                ].get("amount", 0)
        nutrient_list = []

        for nutrient in nutrient_dict.values():
            nutrient_daily_value_dto = Nutrient_Daily_Value_DTO(
                nutrient_id=nutrient["nutrient_id"],
                daily_value=nutrient["amount"]
                / nutrient["usda_nutrient_daily_value_amount"],
                nutrient_unit=nutrient["nutrient_unit"],
            )
            nutrient_list.append(nutrient_daily_value_dto)
        if hasattr(extended_meal_plan_food, "meal_time"):
            return Meal_Nutrient_Stats_DTO(
                food_id=extended_meal_plan_food.id,
                food_name=extended_meal_plan_food.associated_meal.name,
                meal_plan_id=extended_meal_plan_food.meal_plan_id,
                nutrients=nutrient_list,
                meal_time=extended_meal_plan_food.associated_meal.meal_time,
            )
        else:
            return Food_Nutrient_Stats_DTO(
                food_id=extended_meal_plan_food.id,
                food_name=extended_meal_plan_food.associated_snack.name,
                meal_plan_id=extended_meal_plan_food.meal_plan_id,
                nutrients=nutrient_list,
            )
