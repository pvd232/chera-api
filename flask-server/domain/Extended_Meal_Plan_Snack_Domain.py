from domain.Meal_Plan_Snack_Domain import Meal_Plan_Snack_Domain
from domain.Extended_Recipe_Ingredient_Domain import Extended_Recipe_Ingredient_Domain
from domain.Snack_Domain import Snack_Domain
from domain.Extended_Meal_Plan_Domain import Extended_Meal_Plan_Domain
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models import Meal_Plan_Snack_Model


class Extended_Meal_Plan_Snack_Domain(Meal_Plan_Snack_Domain):
    def __init__(self, meal_plan_snack_model: "Meal_Plan_Snack_Model") -> None:
        super().__init__(meal_plan_snack_object=meal_plan_snack_model)
        self.recipe: list[Extended_Recipe_Ingredient_Domain] = [
            Extended_Recipe_Ingredient_Domain(recipe_ingredient_model=x)
            for x in meal_plan_snack_model.recipe
        ]

        self.associated_snack = Snack_Domain(
            snack_object=meal_plan_snack_model.associated_snack
        )
        self.associated_meal_plan = Extended_Meal_Plan_Domain(
            meal_plan_model=meal_plan_snack_model.associated_meal_plan
        )
