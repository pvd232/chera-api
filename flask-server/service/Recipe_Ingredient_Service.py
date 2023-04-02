from domain.Recipe_Ingredient_Domain import Recipe_Ingredient_Domain
import json
from uuid import UUID
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from repository.Recipe_Ingredient_Repository import Recipe_Ingredient_Repository
    from dto.Recipe_Ingredient_DTO import Recipe_Ingredient_DTO


class Recipe_Ingredient_Service(object):
    def __init__(self, recipe_ingredient_repository: 'Recipe_Ingredient_Repository') -> None:
        self.recipe_ingredient_repository = recipe_ingredient_repository

    def get_recipe_ingredient(self, recipe_ingredient_id: str) -> Recipe_Ingredient_Domain:
        return Recipe_Ingredient_Domain(recipe_ingredient_object=self.recipe_ingredient_repository.get_recipe_ingredient(recipe_ingredient_id=recipe_ingredient_id))

    def get_recipe_ingredients(self) -> list[Recipe_Ingredient_Domain]:
        recipe_ingredient_domains: list[Recipe_Ingredient_Domain] = [Recipe_Ingredient_Domain(
            recipe_ingredient_object=x) for x in self.recipe_ingredient_repository.get_recipe_ingredients()]
        return recipe_ingredient_domains

    def get_meal_plan_meal_recipe_ingredients(self, meal_plan_meal_id: UUID) -> list[Recipe_Ingredient_Domain]:
        recipe_ingredient_domains: list[Recipe_Ingredient_Domain] = [Recipe_Ingredient_Domain(
            recipe_ingredient_object=x) for x in self.recipe_ingredient_repository.get_meal_plan_meal_recipe_ingredients(meal_plan_meal_id=meal_plan_meal_id)]
        return recipe_ingredient_domains

    def create_recipe_ingredients(self, recipe_ingredient_dtos: list['Recipe_Ingredient_DTO']) -> None:
        recipe_ingredient_domains = [Recipe_Ingredient_Domain(
            recipe_ingredient_object=x) for x in recipe_ingredient_dtos]
        self.recipe_ingredient_repository.create_recipe_ingredients(
            recipe_ingredient_domains=recipe_ingredient_domains)

    def update_recipe_ingredients(self, recipe_ingredient_dtos: list['Recipe_Ingredient_DTO']) -> None:
        recipe_ingredient_domains = [Recipe_Ingredient_Domain(
            recipe_ingredient_object=x) for x in recipe_ingredient_dtos]
        self.recipe_ingredient_repository.update_recipe_ingredients(
            recipe_ingredient_domains=recipe_ingredient_domains)

    def write_recipe_ingredients(self) -> None:
        with open("new_recipe_ingredients.json", "r+") as outfile:
            recipe_ingredient_dtos = [x.dto_serialize()
                                      for x in self.get_recipe_ingredients()]
            data = json.load(outfile)
            if data:
                outfile.seek(0)
                json.dump(recipe_ingredient_dtos, outfile, indent=4)
                outfile.truncate()
            else:
                outfile.write(json.dumps(recipe_ingredient_dtos, indent=4))
