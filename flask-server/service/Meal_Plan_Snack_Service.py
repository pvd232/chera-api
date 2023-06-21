from domain.Meal_Plan_Snack_Domain import Meal_Plan_Snack_Domain
from domain.Meal_Plan_Domain import Meal_Plan_Domain
from domain.Recipe_Ingredient_Domain import Recipe_Ingredient_Domain

from uuid import UUID
import json
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from repository.Meal_Plan_Snack_Repository import Meal_Plan_Snack_Repository
    from service.Continuity_Service import Continuity_Service
    from service.Recipe_Ingredient_Service import Recipe_Ingredient_Service
    from service.USDA_Ingredient_Service import USDA_Ingredient_Service
    from models import Meal_Plan_Snack_Model, Meal_Plan_Model
    from dto.Meal_Plan_Snack_DTO import Meal_Plan_Snack_DTO


class Meal_Plan_Snack_Service(object):
    def __init__(
        self, meal_plan_snack_repository: "Meal_Plan_Snack_Repository"
    ) -> None:
        self.meal_plan_snack_repository = meal_plan_snack_repository

    def get_meal_plan_snack(
        self, meal_plan_snack_id: UUID
    ) -> Optional[Meal_Plan_Snack_Domain]:
        meal_plan_snack: Optional[
            Meal_Plan_Snack_Model
        ] = self.meal_plan_snack_repository.get_meal_plan_snack(
            meal_plan_snack_id=meal_plan_snack_id
        )
        meal_plan_snack_domain: Meal_Plan_Snack_Domain = Meal_Plan_Snack_Domain(
            meal_plan_snack_object=meal_plan_snack
        )
        return meal_plan_snack_domain

    def get_meal_plan_snacks(
        self, meal_plan_id: UUID = None
    ) -> Optional[list[Meal_Plan_Snack_Domain]]:
        meal_plan_snacks: Optional[
            list[Meal_Plan_Snack_Model]
        ] = self.meal_plan_snack_repository.get_meal_plan_snacks(
            meal_plan_id=meal_plan_id
        )
        if meal_plan_snacks:
            meal_plan_snack_domains: list[Meal_Plan_Snack_Domain] = [
                Meal_Plan_Snack_Domain(meal_plan_snack_object=x)
                for x in meal_plan_snacks
            ]
            return meal_plan_snack_domains
        else:
            return False

    def create_meal_plan_snack(
        self, meal_plan_snack_dto: "Meal_Plan_Snack_DTO"
    ) -> None:
        meal_plan_snack_domain: Meal_Plan_Snack_Domain = Meal_Plan_Snack_Domain(
            meal_plan_snack_object=meal_plan_snack_dto
        )
        self.meal_plan_snack_repository.create_meal_plan_snack(
            meal_plan_snack_domain=meal_plan_snack_domain
        )
        return

    def update_meal_plan_snacks(
        self,
        meal_plan_snacks: list[dict],
        recipe_ingredient_service: "Recipe_Ingredient_Service",
        usda_ingredient_service: "USDA_Ingredient_Service",
        continuity_service: "Continuity_Service",
    ) -> None:
        meal_plan_snack_domains: list[Meal_Plan_Snack_Domain] = []
        for meal_plan_snack in meal_plan_snacks:
            new_domain: Meal_Plan_Snack_Domain = Meal_Plan_Snack_Domain(
                meal_plan_snack_json=meal_plan_snack
            )
            meal_plan_snack_domains.append(new_domain)

        for meal_plan_snack_domain in meal_plan_snack_domains:
            odd_meal_plan: Meal_Plan_Domain = Meal_Plan_Domain(
                meal_plan_object=self.db.session.query(Meal_Plan_Model)
                .filter(Meal_Plan_Model.id == meal_plan_snack_domain.meal_plan_id)
                .first()
            )
            even_meal_plan: Meal_Plan_Domain = Meal_Plan_Domain(
                meal_plan_object=self.db.session.query(Meal_Plan_Model)
                .filter(Meal_Plan_Model.number == odd_meal_plan.number + 1)
                .first()
            )
            even_meal_plan_snack: Meal_Plan_Snack_Domain = Meal_Plan_Snack_Domain(
                meal_plan_snack_object=self.db.session.query(Meal_Plan_Snack_Model)
                .filter(
                    Meal_Plan_Snack_Model.meal_id == meal_plan_snack_domain.meal_id,
                    Meal_Plan_Snack_Model.meal_plan_id == even_meal_plan.id,
                )
                .first()
            )

            self.meal_plan_snack_repository.update_meal_plan_snack(
                odd_meal_plan_snack=meal_plan_snack_domain,
                even_meal_plan_snack=even_meal_plan_snack,
            )

            for recipe_ingredient in meal_plan_snack_domain.recipe:
                even_recipe_ingredient: Recipe_Ingredient_Domain = [
                    x
                    for x in even_meal_plan_snack.recipe
                    if x.usda_ingredient_id == recipe_ingredient.usda_ingredient_id
                ][0]
                recipe_ingredient_service.update_recipe_ingredient(
                    recipe_ingredient=recipe_ingredient,
                    even_recipe_ingredient=even_recipe_ingredient,
                )
                usda_ingredient_service.update_usda_ingredient(
                    usda_ingredient_id=recipe_ingredient.usda_ingredient_id,
                    recipe_ingredient_domain=recipe_ingredient,
                )
        continuity_service.write_meal_data()

    def write_meal_plan_snacks(self) -> None:
        from pathlib import Path
        from utils.write_json import write_json

        meal_plan_snack_json_file = Path(
            ".", "nutrient_data", "new_meal_plan_snacks.json"
        )
        with open(meal_plan_snack_json_file, "r+") as outfile:
            meal_plan_snack_dtos = [x.serialize() for x in self.get_meal_plan_snacks()]
            write_json(outfile=outfile, dicts=meal_plan_snack_dtos)
