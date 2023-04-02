from uuid import UUID
from typing import TYPE_CHECKING
from .Base_DTO import Base_DTO
if TYPE_CHECKING:
    from domain.Staged_Client_Domain import Staged_Client_Domain


class Staged_Client_DTO(Base_DTO):
    def __init__(self, staged_client_json: dict = None, staged_client_domain: 'Staged_Client_Domain' = None) -> None:
        if staged_client_json:
            self.id: str = staged_client_json["id"]
            self.first_name: str = staged_client_json["first_name"]
            self.dietitian_id: str = staged_client_json["dietitian_id"]
            self.meal_plan_id: UUID = staged_client_json["meal_plan_id"]
            self.notes: str = staged_client_json["notes"]
            self.datetime: float = float(staged_client_json["datetime"])
            self.account_created: bool = staged_client_json["account_created"]
            self.active: bool = staged_client_json["active"]
            self.waitlisted: bool = staged_client_json["waitlisted"]
            self.meals_pre_selected: bool = staged_client_json["meals_pre_selected"]
            self.meals_prepaid: bool = staged_client_json["meals_prepaid"]
        elif staged_client_domain:
            self.id: str = staged_client_domain.id
            self.first_name: str = staged_client_domain.first_name
            self.dietitian_id: str = staged_client_domain.dietitian_id
            self.meal_plan_id: UUID = staged_client_domain.meal_plan_id
            self.notes: str = staged_client_domain.notes
            self.datetime: float = staged_client_domain.datetime
            self.account_created: bool = staged_client_domain.account_created
            self.active: bool = staged_client_domain.active
            self.waitlisted: bool = staged_client_domain.waitlisted
            self.meals_pre_selected: bool = staged_client_domain.meals_pre_selected
            self.meals_prepaid: bool = staged_client_domain.meals_prepaid
