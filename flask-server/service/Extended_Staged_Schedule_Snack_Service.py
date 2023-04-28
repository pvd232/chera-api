from .Staged_Schedule_Snack_Service import Staged_Schedule_Snack_Service
from domain.Staged_Schedule_Snack_Domain import Staged_Schedule_Snack_Domain
from domain.Extended_Staged_Schedule_Snack_Domain import (
    Extended_Staged_Schedule_Snack_Domain,
)
from uuid import UUID
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from models import Staged_Schedule_Snack_Model


class Extended_Staged_Schedule_Snack_Service(Staged_Schedule_Snack_Service):
    def get_extended_staged_schedule_snacks(
        self, meal_subscription_id: UUID
    ) -> Optional[list["Extended_Staged_Schedule_Snack_Domain"]]:
        staged_schedule_snacks: Optional[
            list["Staged_Schedule_Snack_Model"]
        ] = self.staged_schedule_snack_repository.get_staged_schedule_snacks(
            meal_subscription_id=meal_subscription_id
        )
        if staged_schedule_snacks:
            return [
                Extended_Staged_Schedule_Snack_Domain(staged_schedule_snack_model=x)
                for x in staged_schedule_snacks
            ]
        else:
            return None
