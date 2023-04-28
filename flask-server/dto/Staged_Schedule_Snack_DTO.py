from .Base_DTO import Base_DTO

from typing import TYPE_CHECKING
from uuid import UUID

if TYPE_CHECKING:
    from domain.Staged_Schedule_Snack_Domain import Staged_Schedule_Snack_Domain


class Staged_Schedule_Snack_DTO(Base_DTO):
    def __init__(
        self,
        staged_schedule_snack_json: dict = None,
        staged_schedule_snack_domain: "Staged_Schedule_Snack_Domain" = None,
    ) -> None:
        if staged_schedule_snack_json:
            self.id: UUID = UUID(staged_schedule_snack_json["id"])
            self.snack_id: UUID = UUID(staged_schedule_snack_json["snack_id"])
            self.staged_client_id: str = staged_schedule_snack_json["staged_client_id"]
        elif staged_schedule_snack_domain:
            self.id: UUID = staged_schedule_snack_domain.id
            self.snack_id: UUID = staged_schedule_snack_domain.snack_id
            self.staged_client_id: str = staged_schedule_snack_domain.staged_client_id
