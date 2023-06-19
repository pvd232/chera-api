from repository.Base_Repository import Base_Repository
from models import Imperial_Unit_Model
from sqlalchemy import inspect


class Imperial_Unit_Repository(Base_Repository):
    def get_imperial_units(self) -> list[Imperial_Unit_Model]:
        imperial_units = self.db.session.query(Imperial_Unit_Model).all()
        return imperial_units

    def initialize_imperial_units(self) -> None:
        from pathlib import Path
        from utils.load_json import load_json
        from domain.Imperial_Unit_Domain import Imperial_Unit_Domain
        from dto.Imperial_Unit_DTO import Imperial_Unit_DTO

        imperial_unit_json_file = Path(".", "nutrient_data", "new_imperial_units.json")
        imperial_units_data = load_json(filename=imperial_unit_json_file)

        # Only initialize custom values, not USDA values which are initialized alongside Imperial_unit_Models
        for imperial_unit_json in imperial_units_data:
            imperial_unit_dto = Imperial_Unit_DTO(imperial_unit_json=imperial_unit_json)
            imperial_unit_domain = Imperial_Unit_Domain(
                imperial_unit_object=imperial_unit_dto
            )

            new_imperial_unit_model = Imperial_Unit_Model(
                imperial_unit_domain=imperial_unit_domain
            )
            self.db.session.add(new_imperial_unit_model)
        self.db.session.commit()
