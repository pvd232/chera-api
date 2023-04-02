from dto.Client_DTO import Client_DTO
from dto.Meal_Plan_DTO import Meal_Plan_DTO
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from domain.Extended_Client_Domain import Extended_Client_Domain


class Extended_Client_DTO(Client_DTO):
    def __init__(self, extended_client_domain: 'Extended_Client_Domain' = None) -> None:
        super().__init__(client_domain=extended_client_domain)
        self.meal_plan = Meal_Plan_DTO(
            meal_plan_domain=extended_client_domain.meal_plan)
