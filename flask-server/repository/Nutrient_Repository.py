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
