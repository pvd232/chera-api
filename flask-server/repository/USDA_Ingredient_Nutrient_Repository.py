from repository.Base_Repository import Base_Repository
from models import USDA_Ingredient_Nutrient_Model
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from domain.USDA_Ingredient_Nutrient_Domain import USDA_Ingredient_Nutrient_Domain


class USDA_Ingredient_Nutrient_Repository(Base_Repository):
    def get_usda_ingredient_nutrients(
        self, usda_ingredient_id: str
    ) -> list[USDA_Ingredient_Nutrient_Model]:
        usda_ingredient_nutrients = (
            self.db.session.query(USDA_Ingredient_Nutrient_Model)
            .filter(
                USDA_Ingredient_Nutrient_Model.usda_ingredient_id == usda_ingredient_id
            )
            .all()
        )
        return usda_ingredient_nutrients

    def get_all_usda_ingredient_nutrients(
        self,
    ) -> list[USDA_Ingredient_Nutrient_Model]:
        usda_ingredient_nutrients = self.db.session.query(
            USDA_Ingredient_Nutrient_Model
        ).all()
        return usda_ingredient_nutrients

    def create_usda_ingredient_nutrient(
        self, usda_ingredient_nutrient_domain: "USDA_Ingredient_Nutrient_Domain"
    ) -> None:
        usda_ingredient_nutrient = USDA_Ingredient_Nutrient_Model(
            usda_ingredient_nutrient_domain=usda_ingredient_nutrient_domain
        )
        self.db.session.add(usda_ingredient_nutrient)
        self.db.session.commit()

    def create_usda_ingredient_nutrients(
        self, usda_ingredient_nutrient_domains: list["USDA_Ingredient_Nutrient_Domain"]
    ) -> None:
        for usda_ingredient_nutrient_domain in usda_ingredient_nutrient_domains:
            new_usda_ingredient_nutrient = USDA_Ingredient_Nutrient_Model(
                usda_ingredient_nutrient_domain=usda_ingredient_nutrient_domain
            )
            self.db.session.add(new_usda_ingredient_nutrient)
        self.db.session.commit()

    def delete_usda_ingredient_nutrients(self, usda_ingredient_id: str) -> None:
        self.db.session.query(USDA_Ingredient_Nutrient_Model).filter(
            USDA_Ingredient_Nutrient_Model.usda_ingredient_id == usda_ingredient_id
        ).delete()
        self.db.session.commit()

    def initialize_usda_ingredient_nutrients(self) -> None:
        from pathlib import Path
        from utils.load_json import load_json
        from domain.USDA_Ingredient_Nutrient_Domain import (
            USDA_Ingredient_Nutrient_Domain,
        )
        from dto.USDA_Ingredient_Nutrient_DTO import USDA_Ingredient_Nutrient_DTO

        usda_ingredient_nutrient_json_file = Path(
            ".", "nutrient_data", "new_usda_ingredient_nutrients.json"
        )
        usda_ingredient_nutrients_data = load_json(
            filename=usda_ingredient_nutrient_json_file
        )

        # Only initialize custom values, not USDA values which are initialized alongside Nutrient_Models
        for usda_ingredient_nutrient_json in usda_ingredient_nutrients_data:
            usda_ingredient_nutrient_dto = USDA_Ingredient_Nutrient_DTO(
                usda_ingredient_nutrient_json=usda_ingredient_nutrient_json
            )
            usda_ingredient_nutrient_domain = USDA_Ingredient_Nutrient_Domain(
                usda_ingredient_nutrient_object=usda_ingredient_nutrient_dto
            )

            new_usda_ingredient_nutrient_model = USDA_Ingredient_Nutrient_Model(
                usda_ingredient_nutrient_domain=usda_ingredient_nutrient_domain
            )
            self.db.session.add(new_usda_ingredient_nutrient_model)
        self.db.session.commit()
