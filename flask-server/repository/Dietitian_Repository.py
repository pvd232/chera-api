from .Base_Repository import Base_Repository
from models import Dietitian_Model
from werkzeug.security import generate_password_hash, check_password_hash
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from domain.Dietitian_Domain import Dietitian_Domain


class Dietitian_Repository(Base_Repository):
    def get_dietitians(self) -> list[Dietitian_Model]:
        dietitians = self.db.session.query(Dietitian_Model).all()
        return dietitians

    def update_dietitian_password(self, dietitian_id: str, new_password: str) -> Dietitian_Model:
        dietitian_to_update: Dietitian_Model = self.get_dietitian(
            dietitian_id=dietitian_id)
        dietitian_to_update.password = generate_password_hash(new_password)
        self.db.session.commit()
        return dietitian_to_update

    def get_dietitian(self, dietitian_id: str) -> Optional[Dietitian_Model]:
        dietitian = self.db.session.query(Dietitian_Model).filter(
            Dietitian_Model.id == dietitian_id).first()
        return dietitian

    def authenticate_dietitian(self, dietitian_id: str, password: str) -> Optional[Dietitian_Model]:
        for dietitian in self.db.session.query(Dietitian_Model):
            if dietitian.id == dietitian_id and check_password_hash(dietitian.password, password):
                return dietitian
        else:
            return None

    def create_dietitian(self, dietitian: 'Dietitian_Domain') -> Dietitian_Model:
        new_dietitian: Dietitian_Model = Dietitian_Model(
            dietitian_domain=dietitian)
        self.db.session.add(new_dietitian)
        self.db.session.commit()
        return new_dietitian
