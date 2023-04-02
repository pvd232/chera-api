from repository.Base_Repository import Base_Repository
from models import Recipe_Ingredient_Model
from uuid import UUID
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from domain.Recipe_Ingredient_Domain import Recipe_Ingredient_Domain


class Recipe_Ingredient_Repository(Base_Repository):
    def get_recipe_ingredient(self, recipe_ingredient_id: str) -> Recipe_Ingredient_Model | None:
        recipe_ingredient = self.db.session.query(Recipe_Ingredient_Model).filter(
            Recipe_Ingredient_Model.id == recipe_ingredient_id).first()
        return recipe_ingredient

    def get_recipe_ingredients(self) -> Optional[list[Recipe_Ingredient_Model]]:
        recipe_ingredients = self.db.session.query(
            Recipe_Ingredient_Model).all()
        return recipe_ingredients

    def get_meal_plan_meal_recipe_ingredients(self, meal_plan_meal_id: UUID) -> list[Recipe_Ingredient_Model]:
        recipe_ingredients = self.db.session.query(
            Recipe_Ingredient_Model).filter(Recipe_Ingredient_Model.meal_plan_meal_id == meal_plan_meal_id).all()
        return recipe_ingredients

    def create_recipe_ingredients(self, recipe_ingredient_domains: list['Recipe_Ingredient_Domain']) -> None:
        for recipe_ingredient_domain in recipe_ingredient_domains:
            recipe_ingredient_to_create = Recipe_Ingredient_Model(
                recipe_ingredient_domain=recipe_ingredient_domain)
            self.db.session.add(recipe_ingredient_to_create)
        self.db.session.commit()

    def update_recipe_ingredients(self, recipe_ingredient_domains: list['Recipe_Ingredient_Domain']) -> None:
        for recipe_ingredient_domain in recipe_ingredient_domains:
            recipe_ingredient_to_update = self.db.session.query(Recipe_Ingredient_Model).filter(
                Recipe_Ingredient_Model.id == recipe_ingredient_domain.id).first()
            recipe_ingredient_to_update.quantity = recipe_ingredient_domain.quantity
        self.db.session.commit()
