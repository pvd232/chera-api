from .Base_Repository import Base_Repository
from models import Dietary_Restriction_Model


class Dietary_Restriction_Repository(Base_Repository):
    def get_dietary_restrictions(self) -> list[Dietary_Restriction_Model]:
        return self.db.session.query(Dietary_Restriction_Model).all()
