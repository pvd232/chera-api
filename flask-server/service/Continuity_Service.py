from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from service.Nutrient_Service import Nutrient_Service
    from service.USDA_Ingredient_Service import USDA_Ingredient_Service
    from service.USDA_Ingredient_Nutrient_Service import USDA_Ingredient_Nutrient_Service
    from service.USDA_Ingredient_Portion_Service import USDA_Ingredient_Portion_Service
    from service.USDA_Nutrient_Daily_Value_Service import USDA_Nutrient_Daily_Value_Service
    from service.Meal_Service import Meal_Service
    from service.Meal_Plan_Service import Meal_Plan_Service
    from service.Meal_Plan_Meal_Service import Meal_Plan_Meal_Service
    from service.Recipe_Ingredient_Service import Recipe_Ingredient_Service
    from service.Recipe_Ingredient_Nutrient_Service import Recipe_Ingredient_Nutrient_Service


class Continuity_Service(object):
    def write_meal_data(self, nutrient_service: 'Nutrient_Service', usda_ingredient_service: 'USDA_Ingredient_Service', usda_ingredient_nutrient_service: 'USDA_Ingredient_Nutrient_Service', usda_ingredient_portion_service: 'USDA_Ingredient_Portion_Service', usda_nutrient_daily_value_service: 'USDA_Nutrient_Daily_Value_Service', meal_service: 'Meal_Service', meal_plan_service: 'Meal_Plan_Service', meal_plan_meal_service: 'Meal_Plan_Meal_Service', recipe_ingredient_service: 'Recipe_Ingredient_Service', recipe_ingredient_nutrient_service: 'Recipe_Ingredient_Nutrient_Service') -> None:
        nutrient_service.write_nutrients()
        usda_ingredient_service.write_usda_ingredients()
        usda_ingredient_nutrient_service.write_usda_ingredient_nutrients()
        usda_ingredient_portion_service.write_usda_ingredient_portions()
        usda_nutrient_daily_value_service.write_usda_nutrient_daily_values()
        meal_service.write_meals()
        meal_plan_service.write_meal_plans()
        meal_plan_meal_service.write_meal_plan_meals()
        recipe_ingredient_service.write_recipe_ingredients()
        recipe_ingredient_nutrient_service.write_recipe_ingredient_nutrients()
