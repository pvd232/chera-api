from repository.Base_Repository import Base_Repository
from models import USDA_Ingredient_Model
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

if TYPE_CHECKING:
    from domain.Recipe_Ingredient_Domain import Recipe_Ingredient_Domain
    from dto.USDA_Nutrient_Mapper_DTO import USDA_Nutrient_Mapper_DTO


class USDA_Ingredient_Repository(Base_Repository):
    def create_ingredient(
        self, usda_nutrient_mapper_dto: "USDA_Nutrient_Mapper_DTO"
    ) -> None:
        new_usda_ingredient = USDA_Ingredient_Model(
            usda_ingredient_nutrient_mapper=usda_nutrient_mapper_dto
        )
        self.db.session.add(new_usda_ingredient)
        self.db.session.commit()

    def get_usda_ingredients(self) -> list[USDA_Ingredient_Model]:
        usda_ingredients = self.db.session.query(USDA_Ingredient_Model).all()
        return usda_ingredients

    def get_usda_ingredient(
        self, usda_ingredient_id: UUID
    ) -> USDA_Ingredient_Model | None:
        usda_ingredient = (
            self.db.session.query(USDA_Ingredient_Model)
            .filter(USDA_Ingredient_Model.id == usda_ingredient_id)
            .first()
        )
        return usda_ingredient

    def update_usda_ingredient(
        self,
        usda_ingredient_id: UUID,
        usda_nutrient_mapper_dto: "USDA_Nutrient_Mapper_DTO",
    ) -> None:
        usda_ingredient_to_update: USDA_Ingredient_Model = (
            self.db.session.query(USDA_Ingredient_Model)
            .filter(USDA_Ingredient_Model.id == usda_ingredient_id)
            .first()
        )
        usda_ingredient_to_update.update(
            usda_nutrient_mapper_dto=usda_nutrient_mapper_dto
        )
        self.db.session.commit()

    def initialize_usda_ingredients(self) -> None:
        from pathlib import Path
        from utils.load_json import load_json
        from domain.USDA_Ingredient_Domain import USDA_Ingredient_Domain
        from dto.USDA_Ingredient_DTO import USDA_Ingredient_DTO

        usda_ingredient_json_file = Path(
            ".", "nutrient_data", "new_usda_ingredients.json"
        )
        usda_ingredients_data = load_json(filename=usda_ingredient_json_file)

        # Only initialize custom values, not USDA values which are initialized alongside USDA_Ingredient_Models
        for usda_ingredient_json in usda_ingredients_data:
            usda_ingredient_dto = USDA_Ingredient_DTO(
                usda_ingredient_json=usda_ingredient_json
            )
            usda_ingredient_domain = USDA_Ingredient_Domain(
                usda_ingredient_object=usda_ingredient_dto
            )

            new_usda_ingredient_model = USDA_Ingredient_Model(
                usda_ingredient_domain=usda_ingredient_domain
            )
            self.db.session.add(new_usda_ingredient_model)
        self.db.session.commit()
