from .Base_Repository import Base_Repository
from models import Client_Model, Staged_Client_Model
from werkzeug.security import generate_password_hash, check_password_hash
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
        self, client_id: str = None, client_stripe_id=None
    ) -> Optional[Client_Model]:
        if client_id:
            client = (
                self.db.session.query(Client_Model)
                .filter(Client_Model.id == client_id)
                .first()
            )
        elif client_stripe_id:
            client = (
                self.db.session.query(Client_Model)
                .filter(Client_Model.stripe_id == client_stripe_id)
                .first()
            )
        return client

    def get_clients(self, dietitian_id: str = None) -> Optional[list[Client_Model]]:
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

    def update_client_meal_plan(self, client_domain: "Client_Domain") -> None:
        client_to_update = (
            self.db.session.query(Client_Model)
            .filter(Client_Model.id == client_domain.id)
            .first()
        )

        client_to_update.meal_plan_id = client_domain.meal_plan_id
        self.db.session.commit()
        return

    def update_client_password(self, client_id: str, new_password: str) -> Client_Model:
        client_to_update: Client_Model = self.get_client(client_id=client_id)
        client_to_update.password = generate_password_hash(new_password)
        self.db.session.commit()
        return client_to_update

    def deactivate_client(self, client_id: str) -> None:
        client_to_update: Client_Model = self.get_client(client_id=client_id)
        client_to_update.active = False
        self.db.session.commit()
        return

    def authenticate_client(
        self, client_id: str, password: str
    ) -> Optional[Client_Model]:
        for client in self.db.session.query(Client_Model).all():
            if client.id == client_id and check_password_hash(
                client.password, password
            ):
                return client
        else:
            return None

    def validate_username(self, username: str, hashed_username: str) -> bool:
        # if a username is passed then we query the db to verify it, if the hashed version is passed then we use the check_password_hash to verify it
        if username and not hashed_username:
            client = (
                self.db.session.query(Client_Model)
                .filter(Client_Model.id == username)
                .first()
            )
            if client:
                return True
            else:
                return False
        elif not username and hashed_username:
            for client in self.db.session.query(Client_Model):
                if check_password_hash(hashed_username, client.id):
                    return True
            return False
        else:
            return False

    def delete_all_clients(self) -> None:
        self.db.session.query(Client_Model).delete()
        self.db.session.commit()
        return
