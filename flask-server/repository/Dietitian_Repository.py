from .Base_Repository import Base_Repository
from models import Dietitian_Model
from uuid import uuid4
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from domain.Dietitian_Domain import Dietitian_Domain


class Dietitian_Repository(Base_Repository):
    def get_dietitians(self) -> list[Dietitian_Model]:
        dietitians = self.db.session.query(Dietitian_Model).all()
        return dietitians

    def get_dietitian(self, dietitian_email: str) -> Optional[Dietitian_Model]:
        dietitian = (
            self.db.session.query(Dietitian_Model)
            .filter(Dietitian_Model.email == dietitian_email)
            .first()
        )
        return dietitian

    def create_dietitian(self, dietitian: "Dietitian_Domain") -> Dietitian_Model:
        new_dietitian: Dietitian_Model = Dietitian_Model(dietitian_domain=dietitian)
        self.db.session.add(new_dietitian)
        self.db.session.commit()
        return new_dietitian

    def initialize_dietitians(self) -> None:
        from pathlib import Path
        from utils.load_json import load_json
        from domain.Dietitian_Domain import Dietitian_Domain
        from dto.Dietitian_DTO import Dietitian_DTO

        dietitian_json_file = Path(".", "dietitian_data", "dietitians.json")
        dietitians_data = load_json(filename=dietitian_json_file)

        # Only initialize custom values, not USDA values which are initialized alongside Dietitian_Models
        for dietitian_json in dietitians_data:
            dietitian_dto = Dietitian_DTO(dietitian_json=dietitian_json)
            dietitian_domain = Dietitian_Domain(dietitian_object=dietitian_dto)

            new_dietitian_model = Dietitian_Model(dietitian_domain=dietitian_domain)
            self.db.session.add(new_dietitian_model)
        self.db.session.commit()

    def delete_dietitian(self, dietitian_email: str) -> None:
        self.db.session.query(Dietitian_Model).filter(
            Dietitian_Model.email == dietitian_email
        ).delete()
        self.db.session.commit()
        return
