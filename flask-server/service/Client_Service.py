from typing import Optional, TYPE_CHECKING
from uuid import UUID
from domain.Client_Domain import Client_Domain

if TYPE_CHECKING:
    from repository.Client_Repository import Client_Repository
    from dto.Client_DTO import Client_DTO


class Client_Service(object):
    def __init__(self, client_repository: "Client_Repository") -> None:
        self.client_repository = client_repository

    def create_client(self, client_dto: "Client_DTO") -> Client_Domain:
        requested_client_domain = Client_Domain(client_object=client_dto)

        client_model = self.client_repository.create_client(
            client_domain=requested_client_domain
        )
        created_client_domain = Client_Domain(client_object=client_model)
        return created_client_domain

    def get_client(
        self,
        client_email: str = None,
        client_stripe_id: str = None,
        client_id: UUID = None,
    ) -> Optional[Client_Domain]:
        if client_email:
            client = self.client_repository.get_client(client_email=client_email)
            if not client:
                return None
            else:
                client_domain = Client_Domain(client_object=client)
        elif client_stripe_id:
            client = self.client_repository.get_client(
                client_stripe_id=client_stripe_id
            )
            if not client:
                return None
            else:
                client_domain = Client_Domain(client_object=client)
        elif client_id:
            client = self.client_repository.get_client(client_id=client_id)
            if not client:
                return None
            else:
                client_domain = Client_Domain(client_object=client)
        return client_domain

    def get_clients(self, dietitian_id: str = None) -> Optional[list[Client_Domain]]:
        client_models = self.client_repository.get_clients(dietitian_id=dietitian_id)
        if client_models:
            return [
                Client_Domain(client_object=x)
                for x in self.client_repository.get_clients(dietitian_id=dietitian_id)
            ]
        else:
            return None

    def update_client(self, client_dto: "Client_DTO") -> Client_Domain:
        client_domain = Client_Domain(client_object=client_dto)
        self.client_repository.update_client(client_domain=client_domain)
        return client_domain

    def update_address(self, client_dto: "Client_DTO") -> Client_Domain:
        client_domain = Client_Domain(client_object=client_dto)
        self.client_repository.update_address(client_domain=client_domain)
        return client_domain

    def update_client_meal_plan(self, client_dto: "Client_DTO") -> None:
        updated_client: Client_Domain = Client_Domain(client_object=client_dto)
        return self.client_repository.update_client_meal_plan(
            client_domain=updated_client
        )

    def update_client_password(
        self, client_id: str, new_password: str
    ) -> Client_Domain:
        return Client_Domain(
            client_object=self.client_repository.update_client_password(
                client_id=client_id, new_password=new_password
            )
        )

    def deactivate_client(self, client_id: str) -> None:
        return self.client_repository.deactivate_client(client_id=client_id)

    def authenticate_client(
        self, client_id: str, password: str
    ) -> Optional[Client_Domain]:
        client_object = self.client_repository.authenticate_client(
            client_id=client_id, password=password
        )
        if client_object:
            client_domain: Client_Domain = Client_Domain(client_object=client_object)
            return client_domain
        else:
            return None
