from .Meal_Plan_Snack_Service import Meal_Plan_Snack_Service
from domain.Extended_Meal_Plan_Snack_Domain import Extended_Meal_Plan_Snack_Domain
from uuid import UUID
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from models import Meal_Plan_Snack_Model
    from dto.Extended_Recipe_Ingredient_DTO import Extended_Recipe_Ingredient_DTO


class Extended_Meal_Plan_Snack_Service(Meal_Plan_Snack_Service):
    def get_standard_extended_meal_plan_snacks(
        self,
    ) -> list["Extended_Meal_Plan_Snack_Domain"]:
        meal_plan_snacks = (
            self.meal_plan_snack_repository.get_standard_meal_plan_snacks()
        )
        if meal_plan_snacks:
            return [
                Extended_Meal_Plan_Snack_Domain(meal_plan_snack_model=x)
                for x in meal_plan_snacks
            ]

    def get_extended_meal_plan_snack(
        self,
        meal_plan_snack_id: Optional[UUID] = None,
        meal_plan_id: Optional[UUID] = None,
        snack_id: Optional[UUID] = None,
    ) -> Extended_Meal_Plan_Snack_Domain:
        return Extended_Meal_Plan_Snack_Domain(
            meal_plan_snack_model=self.meal_plan_snack_repository.get_meal_plan_snack(
                meal_plan_snack_id=meal_plan_snack_id,
                meal_plan_id=meal_plan_id,
                snack_id=snack_id,
            )
        )

    def get_extended_meal_plan_snacks(
        self,
    ) -> Optional[list["Extended_Meal_Plan_Snack_Domain"]]:
        meal_plan_snacks: Optional[list["Meal_Plan_Snack_Model"]] = (
            self.meal_plan_snack_repository.get_meal_plan_snacks()
        )
        if meal_plan_snacks:
            return [
                Extended_Meal_Plan_Snack_Domain(meal_plan_snack_model=x)
                for x in meal_plan_snacks
            ]
        else:
            return None

    def get_specific_extended_meal_plan_snacks(
        self, meal_plan_id: UUID
    ) -> Optional[list["Extended_Meal_Plan_Snack_Domain"]]:
        meal_plan_snacks: Optional[list["Meal_Plan_Snack_Model"]] = (
            self.meal_plan_snack_repository.get_meal_plan_snacks(
                meal_plan_id=meal_plan_id
            )
        )
        if meal_plan_snacks:
            return [
                Extended_Meal_Plan_Snack_Domain(meal_plan_snack_model=x)
                for x in meal_plan_snacks
            ]
        else:
            return None

    def compute_new_meal_plan_snack(
        self,
        meal_plan_snack_id: UUID,
        updated_recipe: list["Extended_Recipe_Ingredient_DTO"],
    ) -> Extended_Meal_Plan_Snack_Domain:
        unaltered_extended_meal_plan_snack_domain = self.get_extended_meal_plan_snack(
            meal_plan_snack_id=meal_plan_snack_id
        )

        updated_recipe_dict = {}
        for recipe_ingredient in updated_recipe:
            updated_recipe_dict[recipe_ingredient.usda_ingredient_id] = (
                recipe_ingredient
            )
        # Update recipe to reflect new recipe
        for recipe_ingredient in unaltered_extended_meal_plan_snack_domain.recipe:
            matching_ingredient = updated_recipe_dict.get(
                recipe_ingredient.usda_ingredient_id
            )
            if matching_ingredient.quantity != recipe_ingredient.quantity:
                difference = matching_ingredient.quantity / recipe_ingredient.quantity
                for nutrient in recipe_ingredient.nutrients:
                    nutrient.amount = nutrient.amount * difference

                recipe_ingredient.quantity = matching_ingredient.quantity
        return unaltered_extended_meal_plan_snack_domain
