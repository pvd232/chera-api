from repository.Base_Repository import Base_Repository
from models import Snack_Model
from uuid import UUID
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from domain.Snack_Domain import Snack_Domain


class Snack_Repository(Base_Repository):
    def get_snack(self, snack_id: UUID) -> Optional[Snack_Model]:
        snack = (
            self.db.session.query(Snack_Model)
            .filter(Snack_Model.id == snack_id)
            .first()
        )
        return snack

    def get_snacks(self) -> Optional[list[Snack_Model]]:
        snacks = self.db.session.query(Snack_Model).all()
        return snacks

    def create_snack(self, snack_domain: "Snack_Domain") -> None:
        new_snack_model = Snack_Model(snack_domain=snack_domain)
        self.db.session.add(new_snack_model)
        self.db.session.commit()
        return

    def initialize_snacks(self) -> None:
        from pathlib import Path
        from utils.load_json import load_json
        from domain.Snack_Domain import Snack_Domain
        from dto.Snack_DTO import Snack_DTO

        snack_json_file = Path(".", "nutrient_data", "new_snacks.json")
        snacks_data = load_json(filename=snack_json_file)

        # Only initialize custom values, not USDA values which are initialized alongside Snack_Models
        for snack_json in snacks_data:
            snack_dto = Snack_DTO(snack_json=snack_json)
            snack_domain = Snack_Domain(snack_object=snack_dto)

            new_snack_model = Snack_Model(snack_domain=snack_domain)
            self.db.session.add(new_snack_model)
        self.db.session.commit()
