from repository.Base_Repository import Base_Repository
from models import NYSAND_Lead
from uuid import uuid4


class NYSAND_Lead_Repository(Base_Repository):
    def create_nysand_lead(self, dietitian_id: str) -> None:
        nysand_lead = NYSAND_Lead(id=uuid4(), dietitian_id=dietitian_id)
        self.db.session.add(nysand_lead)
        self.db.session.commit()
