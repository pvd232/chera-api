from models import Eating_Disorder_Model
from .Base_Repository import Base_Repository


class Eating_Disorder_Repository(Base_Repository):
    def get_eating_disorders(self) -> list[Eating_Disorder_Model]:
        eating_disorder_list = self.db.session.query(Eating_Disorder_Model).all()
        return eating_disorder_list

