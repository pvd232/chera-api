from .Base_Repository import Base_Repository
from models import Client_Model, Staged_Client_Model
from uuid import UUID
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from domain.Client_Domain import Client_Domain


class Client_Repository(Base_Repository):
    def create_client(self, client_domain: "Client_Domain") -> Client_Model:
        client = Client_Model(client_domain=client_domain)
        staged_client: Staged_Client_Model = (
            self.db.session.query(Staged_Client_Model)
            .filter(Staged_Client_Model.id == client_domain.id)
            .first()
        )

        # set these properties using staged client data
        client.notes = staged_client.notes
        client.dietitian_id = staged_client.dietitian_id

        self.db.session.add(client)
        self.db.session.commit()
        return client

    def get_client(
        self, client_email: str = None, client_stripe_id=None, client_id: UUID = None
    ) -> Optional[Client_Model]:
        if client_email:
            client = (
                self.db.session.query(Client_Model)
                .filter(Client_Model.email == client_email)
                .first()
            )
        elif client_stripe_id:
            client = (
                self.db.session.query(Client_Model)
                .filter(Client_Model.stripe_id == client_stripe_id)
                .first()
            )
        elif client_id:
            client = (
                self.db.session.query(Client_Model)
                .filter(Client_Model.id == client_id)
                .first()
            )
        return client

    def get_clients(self, dietitian_id: UUID = None) -> Optional[list[Client_Model]]:
        if dietitian_id:
            clients = (
                self.db.session.query(Client_Model)
                .filter(Client_Model.dietitian_id == dietitian_id)
                .all()
            )
        else:
            clients = self.db.session.query(Client_Model).all()
        return clients

    def update_client(self, client_domain: "Client_Domain"):
        client_to_update: Client_Model = (
            self.db.session.query(Client_Model)
            .filter(Client_Model.id == client_domain.id)
            .first()
        )
        client_to_update.update(client_domain=client_domain)
        self.db.session.commit()

    def update_address(self, client_domain: "Client_Domain") -> None:
        client_to_update: Client_Model = (
            self.db.session.query(Client_Model)
            .filter(Client_Model.id == client_domain.id)
            .first()
        )
        client_to_update.update_address(client_domain=client_domain)
        self.db.session.commit()

    def update_client_meal_plan(self, client_domain: "Client_Domain") -> None:
        client_to_update = (
            self.db.session.query(Client_Model)
            .filter(Client_Model.id == client_domain.id)
            .first()
        )

        client_to_update.meal_plan_id = client_domain.meal_plan_id
        self.db.session.commit()
        return

    def deactivate_client(self, client_id: UUID) -> None:
        client_to_update: Client_Model = self.get_client(client_id=client_id)
        client_to_update.active = False
        self.db.session.commit()
        return
