from .Staged_Schedule_Snack_Domain import Staged_Schedule_Snack_Domain
from domain.Snack_Domain import Snack_Domain
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models import Staged_Schedule_Snack_Model


class Extended_Staged_Schedule_Snack_Domain(Staged_Schedule_Snack_Domain):
    def __init__(
        self, staged_schedule_snack_model: "Staged_Schedule_Snack_Model"
    ) -> None:
        super().__init__(staged_schedule_snack_object=staged_schedule_snack_model)
        self.associated_snack = Snack_Domain(
            snack_object=staged_schedule_snack_model.associated_snack
        )
