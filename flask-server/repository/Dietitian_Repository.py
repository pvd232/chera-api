from .Base_Repository import Base_Repository
from models import Dietitian_Model
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from domain.Dietitian_Domain import Dietitian_Domain


class Dietitian_Repository(Base_Repository):
    def get_dietitians(self) -> list[Dietitian_Model]:
        dietitians = self.db.session.query(Dietitian_Model).all()
        return dietitians

    def get_dietitian(self, dietitian_id: str) -> Optional[Dietitian_Model]:
        dietitian = (
            self.db.session.query(Dietitian_Model)
            .filter(Dietitian_Model.id == dietitian_id)
            .first()
        )
        return dietitian

    def create_dietitian(self, dietitian: "Dietitian_Domain") -> Dietitian_Model:
        new_dietitian: Dietitian_Model = Dietitian_Model(dietitian_domain=dietitian)
        self.db.session.add(new_dietitian)
        self.db.session.commit()
        return new_dietitian
