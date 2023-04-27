from domain.Recipe_Ingredient_Nutrient_Domain import Recipe_Ingredient_Nutrient_Domain
from domain.Recipe_Ingredient_Domain import Recipe_Ingredient_Domain
from dto.Recipe_Ingredient_Nutrient_DTO import Recipe_Ingredient_Nutrient_DTO
from uuid import uuid4, UUID
import json
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from repository.Recipe_Ingredient_Nutrient_Repository import (
        Recipe_Ingredient_Nutrient_Repository,
    )
    from service.Meal_Plan_Meal_Service import Meal_Plan_Meal_Service
    from service.Meal_Plan_Snack_Service import Meal_Plan_Snack_Service
    from service.USDA_Ingredient_Service import USDA_Ingredient_Service
    from service.USDA_Ingredient_Portion_Service import USDA_Ingredient_Portion_Service
    from service.USDA_Ingredient_Nutrient_Service import (
        USDA_Ingredient_Nutrient_Service,
    )
    from service.USDA_Nutrient_Daily_Value_Service import (
        USDA_Nutrient_Daily_Value_Service,
    )
    from service.Nutrient_Service import Nutrient_Service
    from service.Recipe_Ingredient_Service import Recipe_Ingredient_Service
    from dto.Recipe_Ingredient_DTO import Recipe_Ingredient_DTO


class Recipe_Ingredient_Nutrient_Service(object):
    def __init__(
        self,
        recipe_ingredient_nutrient_repository: "Recipe_Ingredient_Nutrient_Repository",
    ) -> None:
        self.recipe_ingredient_nutrient_repository = (
            recipe_ingredient_nutrient_repository
        )

    def get_recipe_ingredient_nutrients(
        self, recipe_ingredient_id: UUID
    ) -> list[Recipe_Ingredient_Domain]:
        recipe_ingredient_nutrient_domains = [
            Recipe_Ingredient_Nutrient_Domain(recipe_ingredient_nutrient_object=x)
            for x in self.recipe_ingredient_nutrient_repository.get_recipe_ingredient_nutrients(
                recipe_ingredient_id=recipe_ingredient_id
            )
        ]
        return recipe_ingredient_nutrient_domains

    def create_recipe_ingredient_nutrients(
        self,
        recipe_ingredient_dtos: list["Recipe_Ingredient_DTO"],
        meal_plan_meal_service: "Meal_Plan_Meal_Service",
        meal_plan_snack_service: "Meal_Plan_Snack_Service",
        usda_ingredient_service: "USDA_Ingredient_Service",
        usda_ingredient_portion_service: "USDA_Ingredient_Portion_Service",
        usda_ingredient_nutrient_service: "USDA_Ingredient_Nutrient_Service",
        nutrient_service: "Nutrient_Service",
        usda_nutrient_daily_value_service: "USDA_Nutrient_Daily_Value_Service",
    ) -> None:
        recipe_ingredient_domains = [
            Recipe_Ingredient_Domain(recipe_ingredient_object=x)
            for x in recipe_ingredient_dtos
        ]
        meal_plan_id = ""
        if recipe_ingredient_domains[0].meal_plan_meal_id is not None:
            meal_plan_id = meal_plan_meal_service.get_meal_plan_meal(
                meal_plan_meal_id=recipe_ingredient_domains[0].meal_plan_meal_id
            ).meal_plan_id
        else:
            meal_plan_id = meal_plan_snack_service.get_meal_plan_snack(
                meal_plan_snack_id=recipe_ingredient_domains[0].meal_plan_snack_id
            ).meal_plan_id

        for recipe_ingredient_domain in recipe_ingredient_domains:
            recipe_ingredient_nutrients_to_create = []

            # get usda ingredient
            usda_ingredient_domain = usda_ingredient_service.get_usda_ingredient(
                usda_ingredient_id=recipe_ingredient_domain.usda_ingredient_id
            )

            # get usda ingredient portion from recipe ingredient portion id
            usda_ingredient_portion = usda_ingredient_portion_service.get_usda_ingredient_portion(
                usda_ingredient_portion_id=recipe_ingredient_domain.usda_ingredient_portion_id
            )

            # get recipe ingredient grams by multiplying usda ingredient portion grams per non metric unit by recipe ingredient quantity
            recipe_ingredient_grams = (
                usda_ingredient_portion.grams_per_non_metric_unit
                * recipe_ingredient_domain.quantity
            )

            # get ratio of recipe ingredient grams to usda ingredient grams
            recipe_ingredient_grams_to_usda_ingredient_grams_ratio = (
                recipe_ingredient_grams / usda_ingredient_domain.amount_of_grams
            )

            # get usda ingredient nutrients
            usda_ingredient_nutrients = (
                usda_ingredient_nutrient_service.get_usda_ingredient_nutrients(
                    usda_ingredient_id=usda_ingredient_domain.id
                )
            )

            # for each nutrient, multiply nutrient amount by recipe ingredient grams ratio and add to recipe ingredient nutrient
            for usda_nutrient in usda_ingredient_nutrients:
                nutrient = nutrient_service.get_nutrient(
                    nutrient_id=usda_nutrient.nutrient_id
                )
                nutrient_amount = (
                    usda_nutrient.amount
                    * recipe_ingredient_grams_to_usda_ingredient_grams_ratio
                )
                recipe_ingredient_nutrient_id = uuid4()
                if not nutrient.has_daily_value:
                    usda_nutrient_daily_value_amount = 0
                else:
                    usda_nutrient_daily_value_amount = (
                        usda_nutrient_daily_value_service.get_usda_nutrient_daily_value(
                            nutrient_id=usda_nutrient.nutrient_id,
                            meal_plan_id=meal_plan_id,
                        ).amount
                    )
                recipe_ingredient_nutrient_object = {
                    "id": recipe_ingredient_nutrient_id,
                    "recipe_ingredient_id": recipe_ingredient_domain.id,
                    "nutrient_id": usda_nutrient.nutrient_id,
                    "amount": nutrient_amount,
                    "usda_nutrient_daily_value_amount": usda_nutrient_daily_value_amount,
                }
                new_recipe_ingredient_nutrient_dto = Recipe_Ingredient_Nutrient_DTO(
                    recipe_ingredient_nutrient_json=recipe_ingredient_nutrient_object
                )
                new_recipe_ingredient_nutrient_domain = Recipe_Ingredient_Nutrient_Domain(
                    recipe_ingredient_nutrient_object=new_recipe_ingredient_nutrient_dto
                )
                recipe_ingredient_nutrients_to_create.append(
                    new_recipe_ingredient_nutrient_domain
                )

            # Create recipe ingredient nutrients
            self.recipe_ingredient_nutrient_repository.create_recipe_ingredient_nutrients(
                recipe_ingredient_nutrient_domains=recipe_ingredient_nutrients_to_create
            )

    def helper_update_recipe_ingredient_nutrients(
        self,
        recipe_ingredient_dtos: list["Recipe_Ingredient_DTO"],
        recipe_ingredient_service: "Recipe_Ingredient_Service",
    ) -> None:
        nutrients_to_update = []
        updated_recipe_ingredient_domains = [
            Recipe_Ingredient_Domain(recipe_ingredient_object=x)
            for x in recipe_ingredient_dtos
        ]
        original_recipe_ingredient_domains = (
            recipe_ingredient_service.get_meal_plan_meal_recipe_ingredients(
                meal_plan_meal_id=updated_recipe_ingredient_domains[0].meal_plan_meal_id
            )
        )

        original_recipe_ingredient_dict = {}
        for original_recipe_ingredient in original_recipe_ingredient_domains:
            original_recipe_ingredient_dict[
                original_recipe_ingredient.id
            ] = original_recipe_ingredient

        for updated_recipe_ingredient in updated_recipe_ingredient_domains:
            updated_nutrients = []
            original_recipe_ingredient = original_recipe_ingredient_dict[
                updated_recipe_ingredient.id
            ]
            if (
                original_recipe_ingredient.quantity
                != updated_recipe_ingredient.quantity
            ):
                recipe_ingredient_nutrients = self.get_recipe_ingredient_nutrients(
                    recipe_ingredient_id=updated_recipe_ingredient.id
                )
                for recipe_ingredient_nutrient in recipe_ingredient_nutrients:
                    recipe_ingredient_nutrient.amount = (
                        recipe_ingredient_nutrient.amount
                        * (
                            updated_recipe_ingredient.quantity
                            / original_recipe_ingredient.quantity
                        )
                    )
                    updated_nutrients.append(recipe_ingredient_nutrient)
                nutrients_to_update.append(updated_nutrients)
        return nutrients_to_update

    def update_recipe_ingredient_nutrients(
        self,
        recipe_ingredient_dtos: list["Recipe_Ingredient_DTO"],
        recipe_ingredient_service: "Recipe_Ingredient_Service",
    ) -> None:
        nutrients_to_update = self.helper_update_recipe_ingredient_nutrients(
            recipe_ingredient_dtos=recipe_ingredient_dtos,
            recipe_ingredient_service=recipe_ingredient_service,
        )
        for nutrients in nutrients_to_update:
            self.recipe_ingredient_nutrient_repository.update_recipe_ingrient_nutrients(
                recipe_ingredient_nutrient_domains=nutrients
            )

    def write_recipe_ingredient_nutrients(self) -> None:
        with open("new_recipe_ingredient_nutrients.json", "r+") as outfile:
            recipe_ingredient_nutrient_dtos = [
                x.dto_serialize() for x in self.get_recipe_ingredient_nutrients()
            ]
            data = json.load(outfile)
            if data:
                outfile.seek(0)
                json.dump(recipe_ingredient_nutrient_dtos, outfile, indent=4)
                outfile.truncate()
            else:
                outfile.write(json.dumps(recipe_ingredient_nutrient_dtos, indent=4))
