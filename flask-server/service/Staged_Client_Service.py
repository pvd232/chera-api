from domain.Staged_Client_Domain import Staged_Client_Domain
from typing import Optional, TYPE_CHECKING
from uuid import UUID

if TYPE_CHECKING:
    from repository.Staged_Client_Repository import Staged_Client_Repository
    from dto.Staged_Client_DTO import Staged_Client_DTO


class Staged_Client_Service(object):
    def __init__(self, staged_client_repository: "Staged_Client_Repository") -> None:
        self.staged_client_repository = staged_client_repository

    def create_staged_client(self, staged_client_dto: "Staged_Client_DTO") -> None:
        staged_client_domain = Staged_Client_Domain(
            staged_client_object=staged_client_dto
        )
        new_staged_client_model = self.staged_client_repository.create_staged_client(
            staged_client_domain=staged_client_domain
        )
        new_staged_client_domain = Staged_Client_Domain(
            staged_client_object=new_staged_client_model
        )
        return new_staged_client_domain

    def get_staged_client(
        self, staged_client_email: str = None, staged_client_id: UUID = None
    ) -> Optional[Staged_Client_Domain]:
        staged_client = None
        if staged_client_email:
            staged_client = self.staged_client_repository.get_staged_client(
                staged_client_email=staged_client_email
            )
        elif staged_client_id:
            staged_client = self.staged_client_repository.get_staged_client(
                staged_client_id=staged_client_id
            )
        if staged_client:
            staged_client_domain = Staged_Client_Domain(
                staged_client_object=staged_client
            )
            return staged_client_domain
        else:
            return False

    def get_staged_clients(self, dietitian_id: str) -> list[Staged_Client_Domain]:
        return [
            Staged_Client_Domain(staged_client_object=x)
            for x in self.staged_client_repository.get_staged_clients(
                dietitian_id=dietitian_id
            )
        ]

    def update_staged_client_account_status(self, staged_client_id: str) -> None:
        return self.staged_client_repository.update_staged_client_account_status(
            staged_client_id=staged_client_id
        )

    def update_staged_client_meal_plan(
        self, staged_client_dto: "Staged_Client_DTO"
    ) -> None:
        updated_staged_client: Staged_Client_Domain = Staged_Client_Domain(
            staged_client_object=staged_client_dto
        )
        return self.staged_client_repository.update_staged_client_meal_plan(
            staged_client_domain=updated_staged_client
        )

    def add_staged_client_to_waitlist(self, staged_client_id: str) -> None:
        return self.staged_client_repository.add_staged_client_to_waitlist(
            staged_client_id=staged_client_id
        )
