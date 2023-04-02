from repository.Base_Repository import Base_Repository
from models import Dietitian_Prepayment_Model
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from domain.Dietitian_Prepayment_Domain import Dietitian_Prepayment_Domain


class Dietitian_Prepayment_Repository(Base_Repository):
    def create_dietitian_prepayment(self,  dietiitan_prepayment_domain: 'Dietitian_Prepayment_Domain') -> None:
        new_dietitian_prepayment = Dietitian_Prepayment_Model(
            dietitian_prepayment_domain=dietiitan_prepayment_domain)
        self.db.session.add(new_dietitian_prepayment)
        self.db.session.commit()
