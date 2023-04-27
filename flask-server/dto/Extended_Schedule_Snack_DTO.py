from dto.Schedule_Snack_DTO import Schedule_Snack_DTO
from dto.Snack_DTO import Snack_DTO
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from domain.Extended_Schedule_Snack_Domain import Extended_Schedule_Snack_Domain


class Extended_Schedule_Snack_DTO(Schedule_Snack_DTO):
    def __init__(
        self, extended_schedule_snack_domain: "Extended_Schedule_Snack_Domain" = None
    ) -> None:
        super().__init__(schedule_snack_domain=extended_schedule_snack_domain)
        self.associated_snack = Snack_DTO(
            extended_snack_domain=extended_schedule_snack_domain.associated_snack
        )
