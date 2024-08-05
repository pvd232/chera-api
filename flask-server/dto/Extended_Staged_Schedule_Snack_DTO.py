from dto.Staged_Schedule_Snack_DTO import Staged_Schedule_Snack_DTO
from dto.Snack_DTO import Snack_DTO
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from domain.Extended_Staged_Schedule_Snack_Domain import (
        Extended_Staged_Schedule_Snack_Domain,
    )


class Extended_Staged_Schedule_Snack_DTO(Staged_Schedule_Snack_DTO):
    def __init__(
        self,
        extended_staged_schedule_snack_domain: Optional[
            Extended_Staged_Schedule_Snack_Domain
        ] = None,
    ) -> None:
        super().__init__(
            staged_schedule_snack_domain=extended_staged_schedule_snack_domain
        )
        self.associated_snack = Snack_DTO(
            snack_domain=extended_staged_schedule_snack_domain.associated_snack
        )
