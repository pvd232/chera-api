from repository.Base_Repository import Base_Repository
from models import Nutrient_Model
from typing import Optional


class Nutrient_Repository(Base_Repository):
    def get_nutrient(self, nutrient_id: str) -> Optional[Nutrient_Model]:
        nutrient = self.db.session.query(Nutrient_Model).filter(
            Nutrient_Model.id == nutrient_id).first()
        return nutrient

    def get_nutrients(self) -> list[Nutrient_Model]:
        nutrients = self.db.session.query(Nutrient_Model).all()
        return nutrients
    
    def initialize_nutrients(self) -> None:
        from pathlib import Path
        from utils.load_json import load_json
        from domain.Nutrient_Domain import Nutrient_Domain
        from dto.Nutrient_DTO import Nutrient_DTO

        nutrient_json_file = Path(".", "nutrient_data", "new_nutrients.json")
        nutrients_data = load_json(filename=nutrient_json_file)

        # Only initialize custom values, not USDA values which are initialized alongside Nutrient_Models
        for nutrient_json in nutrients_data:
            nutrient_dto = Nutrient_DTO(nutrient_json=nutrient_json)
            nutrient_domain = Nutrient_Domain(nutrient_object=nutrient_dto)

            new_nutrient_model = Nutrient_Model(nutrient_domain=nutrient_domain)
            self.db.session.add(new_nutrient_model)
        self.db.session.commit()
