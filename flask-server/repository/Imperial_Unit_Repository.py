from repository.Base_Repository import Base_Repository
from models import Imperial_Unit_Model


class Imperial_Unit_Repository(Base_Repository):
    def get_imperial_units(self) -> list[Imperial_Unit_Model]:
        imperial_units = self.db.session.query(Imperial_Unit_Model).all()
        return imperial_units
