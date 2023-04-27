from domain.Extended_Order_Snack_Domain import Extended_Order_Snack_Domain
from dto.Order_Snack_DTO import Order_Snack_DTO
from dto.Extended_Scheduled_Order_Snack_DTO import Extended_Scheduled_Order_Snack_DTO


class Extended_Order_Snack_DTO(Order_Snack_DTO):
    def __init__(
        self, extended_order_snack_domain: Extended_Order_Snack_Domain
    ) -> None:
        super().__init__(order_snack_domain=extended_order_snack_domain)
        self.scheduled_order_snack: Extended_Scheduled_Order_Snack_DTO = Extended_Scheduled_Order_Snack_DTO(
            extended_scheduled_order_snack_domain=extended_order_snack_domain.scheduled_order_snack
        )
