from domain.Staged_Schedule_Snack_Domain import Staged_Schedule_Snack_Domain
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from repository.Staged_Schedule_Snack_Repository import (
        Staged_Schedule_Snack_Repository,
    )
    from dto.Staged_Schedule_Snack_DTO import Staged_Schedule_Snack_DTO


class Staged_Schedule_Snack_Service(object):
    def __init__(
        self, staged_schedule_snack_repository: "Staged_Schedule_Snack_Repository"
    ) -> None:
        self.staged_schedule_snack_repository = staged_schedule_snack_repository

    def create_staged_schedule_snacks(
        self, staged_schedule_snack_dtos: list["Staged_Schedule_Snack_DTO"]
    ) -> None:
        staged_schedule_snack_domains: list[Staged_Schedule_Snack_Domain] = [
            Staged_Schedule_Snack_Domain(staged_schedule_snack_object=x)
            for x in staged_schedule_snack_dtos
        ]
        self.staged_schedule_snack_repository.create_staged_schedule_snacks(
            staged_schedule_snack_domains=staged_schedule_snack_domains
        )

    def get_staged_schedule_snacks(
        self, staged_client_id: str
    ) -> Optional[list[Staged_Schedule_Snack_Domain]]:
        staged_schedule_snack_models = (
            self.staged_schedule_snack_repository.get_staged_schedule_snacks(
                staged_client_id=staged_client_id
            )
        )
        if staged_schedule_snack_models:
            staged_schedule_snack_domains: list[Staged_Schedule_Snack_Domain] = [
                Staged_Schedule_Snack_Domain(staged_schedule_snack_object=x)
                for x in staged_schedule_snack_models
            ]
        return staged_schedule_snack_domains
