from repository.Base_Repository import Base_Repository
from models import Recipe_Ingredient_Nutrient_Model
from uuid import UUID
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from domain.Recipe_Ingredient_Nutrient_Domain import (
        Recipe_Ingredient_Nutrient_Domain,
    )


class Recipe_Ingredient_Nutrient_Repository(Base_Repository):
    def get_recipe_ingredient_nutrients(
        self, recipe_ingredient_id: UUID
    ) -> list["Recipe_Ingredient_Nutrient_Domain"]:
        recipe_ingredient_nutrients = (
            self.db.session.query(Recipe_Ingredient_Nutrient_Model)
            .filter(
                Recipe_Ingredient_Nutrient_Model.recipe_ingredient_id
                == recipe_ingredient_id
            )
            .all()
        )
        return recipe_ingredient_nutrients
    def get_all_recipe_ingredient_nutrients(self):
        recipe_ingredient_nutrients = (
            self.db.session.query(Recipe_Ingredient_Nutrient_Model)
            .all()
        )
        return recipe_ingredient_nutrients
    def create_recipe_ingredient_nutrients(
        self,
        recipe_ingredient_nutrient_domains: list["Recipe_Ingredient_Nutrient_Domain"],
    ) -> None:
        for recipe_ingrient_nutrient_domain in recipe_ingredient_nutrient_domains:
            recipe_ingredient_nutrient_model = Recipe_Ingredient_Nutrient_Model(
                recipe_ingredient_nutrient_domain=recipe_ingrient_nutrient_domain
            )
            self.db.session.add(recipe_ingredient_nutrient_model)
        self.db.session.commit()
        return

    def update_recipe_ingrient_nutrients(
        self,
        recipe_ingredient_nutrient_domains: list["Recipe_Ingredient_Nutrient_Domain"],
    ) -> None:
        for recipe_ingredient_nutrient_domain in recipe_ingredient_nutrient_domains:
            recipe_ingredient_nutrient_model = (
                self.db.session.query(Recipe_Ingredient_Nutrient_Model)
                .filter(
                    Recipe_Ingredient_Nutrient_Model.id
                    == recipe_ingredient_nutrient_domain.id
                )
                .first()
            )
            recipe_ingredient_nutrient_model.amount = (
                recipe_ingredient_nutrient_domain.amount
            )
        self.db.session.commit()
        return

    def initialize_recipe_ingredient_nutrients(self) -> None:
        from pathlib import Path
        from utils.load_json import load_json
        from domain.Recipe_Ingredient_Nutrient_Domain import (
            Recipe_Ingredient_Nutrient_Domain,
        )
        from dto.Recipe_Ingredient_Nutrient_DTO import Recipe_Ingredient_Nutrient_DTO

        recipe_ingredient_nutrient_json_file = Path(
            ".", "nutrient_data", "new_recipe_ingredient_nutrients.json"
        )
        recipe_ingredient_nutrients_data = load_json(
            filename=recipe_ingredient_nutrient_json_file
        )

        # Only initialize custom values, not USDA values which are initialized alongside Recipe_ingredient_nutrient_Models
        for recipe_ingredient_nutrient_json in recipe_ingredient_nutrients_data:
            recipe_ingredient_nutrient_dto = Recipe_Ingredient_Nutrient_DTO(
                recipe_ingredient_nutrient_json=recipe_ingredient_nutrient_json
            )
            recipe_ingredient_nutrient_domain = Recipe_Ingredient_Nutrient_Domain(
                recipe_ingredient_nutrient_object=recipe_ingredient_nutrient_dto
            )

            new_recipe_ingredient_nutrient_model = Recipe_Ingredient_Nutrient_Model(
                recipe_ingredient_nutrient_domain=recipe_ingredient_nutrient_domain
            )
            self.db.session.add(new_recipe_ingredient_nutrient_model)
        self.db.session.commit()
