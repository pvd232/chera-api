from .Schedule_Snack_Domain import Schedule_Snack_Domain
from domain.Snack_Domain import Snack_Domain
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models import Schedule_Snack_Model


class Extended_Schedule_Snack_Domain(Schedule_Snack_Domain):
    def __init__(self, schedule_snack_model: "Schedule_Snack_Model") -> None:
        super().__init__(schedule_snack_object=schedule_snack_model)
        self.associated_snack = Snack_Domain(
            snack_model=schedule_snack_model.associated_snack
        )
