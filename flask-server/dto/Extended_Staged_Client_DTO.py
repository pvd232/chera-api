from dto.Staged_Client_DTO import Staged_Client_DTO
from dto.Meal_Plan_DTO import Meal_Plan_DTO
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from domain.Extended_Staged_Client_Domain import Extended_Staged_Client_Domain


class Extended_Staged_Client_DTO(Staged_Client_DTO):
    def __init__(self, extended_staged_client_domain: 'Extended_Staged_Client_Domain' = None) -> None:
        super().__init__(staged_client_domain=extended_staged_client_domain)
        self.meal_plan = Meal_Plan_DTO(
            meal_plan_domain=extended_staged_client_domain.meal_plan)
