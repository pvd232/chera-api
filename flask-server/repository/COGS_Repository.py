from models import COGS_Model
from .Base_Repository import Base_Repository


class COGS_Repository(Base_Repository):
    def get_cogs(self) -> list[COGS_Model]:
        cogs_list = self.db.session.query(COGS_Model).all()
        return cogs_list

    def get_specific_cogs(self, num_items: int, is_local: bool) -> COGS_Model:
        cogs = (
            self.db.session.query(COGS_Model)
            .filter(COGS_Model.num_meals == num_items, COGS_Model.is_local == is_local)
            .first()
        )
        return cogs

    def delete_all_cogs(self):
        self.db.session.query(COGS_Model).delete()
        self.db.session.commit()
