from models import Staged_Client_Model, Dietitian_Model
from .Base_Repository import Base_Repository
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from domain.Staged_Client_Domain import Staged_Client_Domain


class Staged_Client_Repository(Base_Repository):
    def create_staged_client(self, staged_client_domain: 'Staged_Client_Domain') -> None:
        new_staged_client: Staged_Client_Model = Staged_Client_Model(
            staged_client_domain=staged_client_domain)
        self.db.session.add(new_staged_client)
        self.db.session.commit()
        return new_staged_client

    def get_staged_client(self, staged_client_id: str) -> Optional[Staged_Client_Model]:
        staged_client = self.db.session.query(Staged_Client_Model).filter(
            Staged_Client_Model.id == staged_client_id).first()
        return staged_client

    def get_staged_clients(self, dietitian_id: str = None) -> list[Staged_Client_Model]:
        if dietitian_id:
            dietitian = self.db.session.query(Dietitian_Model).filter(
                Dietitian_Model.id == dietitian_id).first()
            staged_clients = dietitian.staged_clients
        else:
            staged_clients = self.db.session.query(Staged_Client_Model).all()
        return staged_clients

    def update_staged_client_account_status(self, staged_client_id: str) -> None:
        staged_client_to_update = self.db.session.query(Staged_Client_Model).filter(
            Staged_Client_Model.id == staged_client_id).first()
        staged_client_to_update.account_created = True
        self.db.session.commit()
        return

    def update_staged_client_meal_plan(self, staged_client_domain: 'Staged_Client_Domain') -> None:
        staged_client_to_update = self.db.session.query(Staged_Client_Model).filter(
            Staged_Client_Model.id == staged_client_domain.id).first()

        staged_client_to_update.meal_plan_id = staged_client_domain.meal_plan_id
        self.db.session.commit()
        return

    def add_staged_client_to_waitlist(self, staged_client_id: str) -> None:
        staged_client_to_update = self.db.session.query(Staged_Client_Model).filter(
            Staged_Client_Model.id == staged_client_id).first()
        staged_client_to_update.waitlisted = True
        self.db.session.commit()
        return

    def delete_all_staged_clients(self) -> None:
        self.db.session.query(Staged_Client_Model).delete()
        self.db.session.commit()
        return
