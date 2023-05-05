from dto.Scheduled_Order_Snack_DTO import Scheduled_Order_Snack_DTO
from dto.Snack_DTO import Snack_DTO
from domain.Extended_Scheduled_Order_Snack_Domain import (
    Extended_Scheduled_Order_Snack_Domain,
)


class Extended_Scheduled_Order_Snack_DTO(Scheduled_Order_Snack_DTO):
    def __init__(
        self,
        extended_scheduled_order_snack_domain: "Extended_Scheduled_Order_Snack_Domain",
    ) -> None:
        super().__init__(
            scheduled_order_snack_domain=extended_scheduled_order_snack_domain
        )
        self.associated_snack: Snack_DTO = Snack_DTO(
            snack_domain=extended_scheduled_order_snack_domain.associated_snack
        )
