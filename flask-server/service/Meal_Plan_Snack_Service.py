from domain.Meal_Plan_Meal_Domain import Meal_Plan_Meal_Domain
from domain.Meal_Plan_Domain import Meal_Plan_Domain
from domain.Recipe_Ingredient_Domain import Recipe_Ingredient_Domain

from uuid import UUID
import json
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from repository.Meal_Plan_Meal_Repository import Meal_Plan_Meal_Repository
    from service.Continuity_Service import Continuity_Service
    from service.Recipe_Ingredient_Service import Recipe_Ingredient_Service
    from service.USDA_Ingredient_Service import USDA_Ingredient_Service
    from models import Meal_Plan_Meal_Model, Meal_Plan_Model
    from dto.Meal_Plan_Meal_DTO import Meal_Plan_Meal_DTO


class Meal_Plan_Meal_Service(object):
    def __init__(self, meal_plan_meal_repository: 'Meal_Plan_Meal_Repository') -> None:
        self.meal_plan_meal_repository = meal_plan_meal_repository

    def get_meal_plan_meal(self, meal_plan_meal_id: UUID) -> Optional[Meal_Plan_Meal_Domain]:
        meal_plan_meal: Optional[Meal_Plan_Meal_Model] = self.meal_plan_meal_repository.get_meal_plan_meal(
            meal_plan_meal_id=meal_plan_meal_id)
        meal_plan_meal_domain: Meal_Plan_Meal_Domain = Meal_Plan_Meal_Domain(
            meal_plan_meal_object=meal_plan_meal)
        return meal_plan_meal_domain

    def get_meal_plan_meals(self, meal_plan_id: UUID = None) -> Optional[list[Meal_Plan_Meal_Domain]]:
        meal_plan_meals: Optional[list[Meal_Plan_Meal_Model]] = self.meal_plan_meal_repository.get_meal_plan_meals(
            meal_plan_id=meal_plan_id)
        if meal_plan_meals:
            meal_plan_meal_domains: list[Meal_Plan_Meal_Domain] = [Meal_Plan_Meal_Domain(meal_plan_meal_object=x)
                                                                   for x in meal_plan_meals]
            return meal_plan_meal_domains
        else:
            return False

    def create_meal_plan_meal(self, meal_plan_meal_dto: 'Meal_Plan_Meal_DTO') -> None:
        meal_plan_meal_domain: Meal_Plan_Meal_Domain = Meal_Plan_Meal_Domain(
            meal_plan_meal_object=meal_plan_meal_dto)
        self.meal_plan_meal_repository.create_meal_plan_meal(
            meal_plan_meal_domain=meal_plan_meal_domain)
        return

    def update_meal_plan_meals(self, meal_plan_meals: list[dict], recipe_ingredient_service: 'Recipe_Ingredient_Service', usda_ingredient_service: 'USDA_Ingredient_Service', continuity_service: 'Continuity_Service') -> None:
        meal_plan_meal_domains: list[Meal_Plan_Meal_Domain] = []
        for meal_plan_meal in meal_plan_meals:
            new_domain: Meal_Plan_Meal_Domain = Meal_Plan_Meal_Domain(
                meal_plan_meal_json=meal_plan_meal)
            meal_plan_meal_domains.append(new_domain)

        for meal_plan_meal_domain in meal_plan_meal_domains:
            odd_meal_plan: Meal_Plan_Domain = Meal_Plan_Domain(meal_plan_object=self.db.session.query(Meal_Plan_Model).filter(
                Meal_Plan_Model.id == meal_plan_meal_domain.meal_plan_id).first())
            even_meal_plan: Meal_Plan_Domain = Meal_Plan_Domain(meal_plan_object=self.db.session.query(Meal_Plan_Model).filter(
                Meal_Plan_Model.number == odd_meal_plan.number + 1).first()
            )
            even_meal_plan_meal: Meal_Plan_Meal_Domain = Meal_Plan_Meal_Domain(meal_plan_meal_object=self.db.session.query(
                Meal_Plan_Meal_Model).filter(Meal_Plan_Meal_Model.meal_id == meal_plan_meal_domain.meal_id, Meal_Plan_Meal_Model.meal_plan_id == even_meal_plan.id).first())

            self.meal_plan_meal_repository.update_meal_plan_meal(
                odd_meal_plan_meal=meal_plan_meal_domain, even_meal_plan_meal=even_meal_plan_meal)

            for recipe_ingredient in meal_plan_meal_domain.recipe:
                even_recipe_ingredient: Recipe_Ingredient_Domain = [
                    x for x in even_meal_plan_meal.recipe if x.usda_ingredient_id == recipe_ingredient.usda_ingredient_id][0]
                recipe_ingredient_service.update_recipe_ingredient(
                    recipe_ingredient=recipe_ingredient, even_recipe_ingredient=even_recipe_ingredient)
                usda_ingredient_service.update_usda_ingredient(
                    usda_ingredient_id=recipe_ingredient.usda_ingredient_id, recipe_ingredient_domain=recipe_ingredient)
        continuity_service.write_meal_data()

    def write_meal_plan_meals(self) -> None:
        with open("new_meal_plan_meals.json", "r+") as outfile:
            meal_plan_meal_dtos = [x.dto_serialize()
                                   for x in self.get_meal_plan_meals()]
            data = json.load(outfile)
            if data:
                outfile.seek(0)
                json.dump(meal_plan_meal_dtos, outfile, indent=4)
                outfile.truncate()
            else:
                outfile.write(json.dumps(meal_plan_meal_dtos, indent=4))
