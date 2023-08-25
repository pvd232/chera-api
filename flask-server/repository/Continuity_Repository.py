from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from repository.Imperial_Unit_Repository import Imperial_Unit_Repository
    from repository.Nutrient_Repository import Nutrient_Repository
    from repository.USDA_Ingredient_Repository import USDA_Ingredient_Repository
    from repository.USDA_Ingredient_Nutrient_Repository import (
        USDA_Ingredient_Nutrient_Repository,
    )
    from repository.USDA_Ingredient_Portion_Repository import (
        USDA_Ingredient_Portion_Repository,
    )
    from repository.USDA_Nutrient_Daily_Value_Repository import (
        USDA_Nutrient_Daily_Value_Repository,
    )
    from repository.Dietary_Restriction_Repository import Dietary_Restriction_Repository
    from repository.Meal_Repository import Meal_Repository
    from repository.Snack_Repository import Snack_Repository
    from repository.Meal_Dietary_Restriction_Repository import (
        Meal_Dietary_Restriction_Repository,
    )
    from repository.Meal_Plan_Repository import Meal_Plan_Repository
    from repository.Meal_Plan_Meal_Repository import Meal_Plan_Meal_Repository
    from repository.Meal_Plan_Snack_Repository import Meal_Plan_Snack_Repository
    from repository.Recipe_Ingredient_Repository import Recipe_Ingredient_Repository
    from repository.Recipe_Ingredient_Nutrient_Repository import (
        Recipe_Ingredient_Nutrient_Repository,
    )
    from repository.Discount_Repository import Discount_Repository
    from repository.Meal_Sample_Repository import Meal_Sample_Repository
    from repository.Meal_Sample_Shipment_Repository import (
        Meal_Sample_Shipment_Repository,
    )


class Continuity_Repository(object):
    def initialize_meal_data(
        self,
        imperial_unit_repository: "Imperial_Unit_Repository",
        nutrient_repository: "Nutrient_Repository",
        usda_ingredient_repository: "USDA_Ingredient_Repository",
        usda_ingredient_nutrient_repository: "USDA_Ingredient_Nutrient_Repository",
        usda_ingredient_portion_repository: "USDA_Ingredient_Portion_Repository",
        usda_nutrient_daily_value_repository: "USDA_Nutrient_Daily_Value_Repository",
        dietary_restriction_repository: "Dietary_Restriction_Repository",
        meal_repository: "Meal_Repository",
        snack_repository: "Snack_Repository",
        meal_dietary_restriction_repository: "Meal_Dietary_Restriction_Repository",
        meal_plan_repository: "Meal_Plan_Repository",
        meal_plan_meal_repository: "Meal_Plan_Meal_Repository",
        meal_plan_snack_repository: "Meal_Plan_Snack_Repository",
        recipe_ingredient_repository: "Recipe_Ingredient_Repository",
        recipe_ingredient_nutrient_repository: "Recipe_Ingredient_Nutrient_Repository",
        discount_repository: "Discount_Repository",
    ) -> None:
        imperial_unit_repository.initialize_imperial_units()
        nutrient_repository.initialize_nutrients()
        usda_ingredient_repository.initialize_usda_ingredients()
        usda_ingredient_nutrient_repository.initialize_usda_ingredient_nutrients()
        usda_ingredient_portion_repository.initialize_usda_ingredient_portions()
        dietary_restriction_repository.initialize_dietary_restrictions()
        meal_repository.initialize_meals()
        snack_repository.initialize_snacks()
        meal_dietary_restriction_repository.initialize_meal_dietary_restrictions()
        meal_plan_repository.initialize_meal_plans()
        usda_nutrient_daily_value_repository.initialize_usda_nutrient_daily_values()
        meal_plan_meal_repository.initialize_meal_plan_meals()
        meal_plan_snack_repository.initialize_meal_plan_snacks()
        recipe_ingredient_repository.initialize_recipe_ingredients()
        recipe_ingredient_nutrient_repository.initialize_recipe_ingredient_nutrients(),
        discount_repository.initialize_discounts()

    def initialize_dietitian_data(
        self,
        meal_sample_repository: "Meal_Sample_Repository",
        meal_sample_shipment_repository: "Meal_Sample_Shipment_Repository",
    ):
        meal_sample_repository.initialize_meal_samples()
        meal_sample_shipment_repository.initialize_meal_sample_shipments()
        return
