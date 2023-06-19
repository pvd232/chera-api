from repository.Base_Repository import Base_Repository
from models import USDA_Ingredient_Portion_Model
from uuid import UUID
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from domain.Recipe_Ingredient_Domain import Recipe_Ingredient_Domain
    from domain.USDA_Ingredient_Portion_Domain import USDA_Ingredient_Portion_Domain


class USDA_Ingredient_Portion_Repository(Base_Repository):
    def get_usda_ingredient_portions(self) -> list[USDA_Ingredient_Portion_Model]:
        usda_ingredient_portions = self.db.session.query(
            USDA_Ingredient_Portion_Model
        ).all()
        return usda_ingredient_portions

    def get_usda_ingredient_portion(
        self,
        usda_ingredient_portion_id: Optional[UUID] = None,
        fda_portion_id: Optional[str] = None,
    ) -> USDA_Ingredient_Portion_Model:
        if usda_ingredient_portion_id:
            usda_ingredient_portion = (
                self.db.session.query(USDA_Ingredient_Portion_Model)
                .filter(USDA_Ingredient_Portion_Model.id == usda_ingredient_portion_id)
                .first()
            )
        else:
            usda_ingredient_portion = (
                self.db.session.query(USDA_Ingredient_Portion_Model)
                .filter(
                    USDA_Ingredient_Portion_Model.fda_portion_id == fda_portion_id,
                    USDA_Ingredient_Portion_Model.custom_value == False,
                )
                .first()
            )
        return usda_ingredient_portion

    def get_recipe_ingredient_portions(
        self, recipe_ingredient_domain: "Recipe_Ingredient_Domain"
    ) -> Optional[list[USDA_Ingredient_Portion_Model]]:
        usda_ingredient_portions = (
            self.db.session.query(USDA_Ingredient_Portion_Model)
            .filter(
                USDA_Ingredient_Portion_Model.usda_ingredient_id
                == recipe_ingredient_domain.usda_ingredient_id
            )
            .all()
        )
        return usda_ingredient_portions

    def create_usda_ingredient_portion(
        self, usda_ingredient_portion_domain: "USDA_Ingredient_Portion_Domain"
    ) -> None:
        new_usda_ingredient_portion = USDA_Ingredient_Portion_Model(
            usda_ingredient_portion_domain=usda_ingredient_portion_domain
        )
        self.db.session.add(new_usda_ingredient_portion)
        self.db.session.commit()

    def initialize_usda_ingredient_portions(self) -> None:
        from pathlib import Path
        from utils.load_json import load_json
        from domain.USDA_Ingredient_Portion_Domain import USDA_Ingredient_Portion_Domain
        from dto.USDA_Ingredient_Portion_DTO import USDA_Ingredient_Portion_DTO

        usda_ingredient_portion_json_file = Path(
            ".", "nutrient_data", "new_usda_ingredient_portions.json"
        )
        usda_ingredient_portions_data = load_json(
            filename=usda_ingredient_portion_json_file
        )

        # Only initialize custom values, not USDA values which are initialized alongside USDA_Ingredient_Models
        for usda_ingredient_portion_json in usda_ingredient_portions_data:
            test_if_exists = (
                self.db.session.query(USDA_Ingredient_Portion_Model).filter(
                    USDA_Ingredient_Portion_Model.id
                    == usda_ingredient_portion_json["id"]
                )
            ).first()
            if not test_if_exists:
                usda_ingredient_portion_dto = USDA_Ingredient_Portion_DTO(
                    usda_ingredient_portion_json=usda_ingredient_portion_json
                )
                usda_ingredient_portion_domain = USDA_Ingredient_Portion_Domain(
                    usda_ingredient_portion_object=usda_ingredient_portion_dto
                )

                new_usda_ingredient_portion_model = USDA_Ingredient_Portion_Model(
                    usda_ingredient_portion_domain=usda_ingredient_portion_domain
                )
                self.db.session.add(new_usda_ingredient_portion_model)
        self.db.session.commit()
