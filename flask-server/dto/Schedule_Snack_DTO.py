from .Base_DTO import Base_DTO
from uuid import UUID
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from domain.Schedule_Snack_Domain import Schedule_Snack_Domain


class Schedule_Snack_DTO(Base_DTO):
    def __init__(
        self,
        schedule_snack_domain: "Schedule_Snack_Domain" = None,
        schedule_snack_json: Optional[dict] = None,
    ) -> None:
        if schedule_snack_json:
            self.id: UUID = UUID(schedule_snack_json["id"])
            self.snack_id: UUID = UUID(schedule_snack_json["snack_id"])
            self.meal_subscription_id: UUID = UUID(
                schedule_snack_json["meal_subscription_id"]
            )
        if schedule_snack_domain:
            self.id: UUID = schedule_snack_domain.id
            self.snack_id: UUID = schedule_snack_domain.snack_id
            self.meal_subscription_id: UUID = schedule_snack_domain.meal_subscription_id
