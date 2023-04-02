from domain.Meal_Plan_Meal_Domain import Meal_Plan_Meal_Domain
from domain.Extended_Recipe_Ingredient_Domain import Extended_Recipe_Ingredient_Domain
from domain.Extended_Meal_Domain import Extended_Meal_Domain
from domain.Extended_Meal_Plan_Domain import Extended_Meal_Plan_Domain
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models import Meal_Plan_Meal_Model


class Extended_Meal_Plan_Meal_Domain(Meal_Plan_Meal_Domain):
    def __init__(self, meal_plan_meal_model: 'Meal_Plan_Meal_Model') -> None:
        super().__init__(meal_plan_meal_object=meal_plan_meal_model)
        self.recipe: list[Extended_Recipe_Ingredient_Domain] = [Extended_Recipe_Ingredient_Domain(
            recipe_ingredient_model=x)for x in meal_plan_meal_model.recipe]

        self.associated_meal = Extended_Meal_Domain(
            meal_model=meal_plan_meal_model.associated_meal)
        self.associated_meal_plan = Extended_Meal_Plan_Domain(
            meal_plan_model=meal_plan_meal_model.associated_meal_plan)
