from .Base_DTO import Base_DTO

from typing import TYPE_CHECKING, Optional
from uuid import UUID

if TYPE_CHECKING:
    from domain.Staged_Schedule_Meal_Domain import Staged_Schedule_Meal_Domain


class Staged_Schedule_Meal_DTO(Base_DTO):
    def __init__(
        self,
        staged_schedule_meal_json: Optional[dict] = None,
        staged_schedule_meal_domain: "Staged_Schedule_Meal_Domain" = None,
    ) -> None:
        if staged_schedule_meal_json:
            self.id: UUID = UUID(staged_schedule_meal_json["id"])
            self.meal_id: UUID = UUID(staged_schedule_meal_json["meal_id"])
            self.staged_client_id: str = staged_schedule_meal_json["staged_client_id"]
        elif staged_schedule_meal_domain:
            self.id: UUID = staged_schedule_meal_domain.id
            self.meal_id: UUID = staged_schedule_meal_domain.meal_id
            self.staged_client_id: str = staged_schedule_meal_domain.staged_client_id
