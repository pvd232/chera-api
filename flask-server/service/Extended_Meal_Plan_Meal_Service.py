from .Meal_Plan_Meal_Service import Meal_Plan_Meal_Service
from domain.Extended_Meal_Plan_Meal_Domain import Extended_Meal_Plan_Meal_Domain
from uuid import UUID
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from dto.Extended_Recipe_Ingredient_DTO import Recipe_Ingredient_DTO


class Extended_Meal_Plan_Meal_Service(Meal_Plan_Meal_Service):
    def get_extended_meal_plan_meal(
        self,
        meal_plan_meal_id: UUID = None,
        meal_plan_id: UUID = None,
        meal_id: UUID = None,
    ) -> Extended_Meal_Plan_Meal_Domain:
        if meal_plan_meal_id:
            return Extended_Meal_Plan_Meal_Domain(
                meal_plan_meal_model=self.meal_plan_meal_repository.get_meal_plan_meal(
                    meal_plan_meal_id=meal_plan_meal_id
                )
            )
        else:
            print("meal_plan_id", meal_plan_id)
            print("meal_id", meal_id)
            return Extended_Meal_Plan_Meal_Domain(
                meal_plan_meal_model=self.meal_plan_meal_repository.get_meal_plan_meal(
                    meal_plan_id=meal_plan_id, meal_id=meal_id
                )
            )

    def get_extended_meal_plan_meals(
        self,
    ) -> Optional[list["Extended_Meal_Plan_Meal_Domain"]]:
        meal_plan_meals = self.meal_plan_meal_repository.get_meal_plan_meals()
        if meal_plan_meals is not None:
            return [
                Extended_Meal_Plan_Meal_Domain(meal_plan_meal_model=x)
                for x in meal_plan_meals
            ]
        else:
            return None

    def get_specific_extended_meal_plan_meals(
        self, meal_plan_id: UUID
    ) -> Optional[list["Extended_Meal_Plan_Meal_Domain"]]:
        meal_plan_meals = self.meal_plan_meal_repository.get_meal_plan_meals(
            meal_plan_id=meal_plan_id
        )
        if meal_plan_meals:
            return [
                Extended_Meal_Plan_Meal_Domain(meal_plan_meal_model=x)
                for x in meal_plan_meals
            ]
        else:
            return None

    def compute_new_meal_plan_meal(
        self,
        meal_plan_meal_id: UUID,
        updated_recipe: list["Recipe_Ingredient_DTO"],
    ) -> Extended_Meal_Plan_Meal_Domain:
        unaltered_extended_meal_plan_meal_domain = self.get_extended_meal_plan_meal(
            meal_plan_meal_id=meal_plan_meal_id,
            meal_plan_id=None,
            meal_id=None,
        )

        updated_recipe_dict: dict[UUID:"Recipe_Ingredient_DTO"] = {}
        for recipe_ingredient in updated_recipe:
            updated_recipe_dict[
                recipe_ingredient.usda_ingredient_id
            ] = recipe_ingredient

        # Update recipe to reflect new recipe
        for recipe_ingredient in unaltered_extended_meal_plan_meal_domain.recipe:
            matching_ingredient = updated_recipe_dict.get(
                str(recipe_ingredient.usda_ingredient_id)
            )
            if matching_ingredient.quantity != recipe_ingredient.quantity:
                difference = matching_ingredient.quantity / recipe_ingredient.quantity
                for nutrient in recipe_ingredient.nutrients:
                    nutrient.amount = nutrient.amount * difference

                recipe_ingredient.quantity = matching_ingredient.quantity
        return unaltered_extended_meal_plan_meal_domain
