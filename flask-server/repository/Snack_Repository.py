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
