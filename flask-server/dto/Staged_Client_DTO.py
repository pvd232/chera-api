from uuid import UUID
from typing import TYPE_CHECKING, Optional
from .Base_DTO import Base_DTO

if TYPE_CHECKING:
    from domain.Staged_Client_Domain import Staged_Client_Domain


class Staged_Client_DTO(Base_DTO):
    def __init__(
        self,
        staged_client_json: dict = None,
        staged_client_domain: "Staged_Client_Domain" = None,
    ) -> None:
        if staged_client_json:
            self.id: UUID = staged_client_json["id"]
            self.email: str = staged_client_json["email"]
            self.dietitian_id: Optional[str] = staged_client_json["dietitian_id"]
            self.meal_plan_id: int = staged_client_json["meal_plan_id"]
            # personal information
            self.first_name: str = staged_client_json["first_name"]
            self.current_weight: int = staged_client_json["current_weight"]
            self.target_weight: float = staged_client_json["target_weight"]
            self.age: str = staged_client_json["age"]
            self.gender: str = staged_client_json["gender"]
            self.notes: str = staged_client_json["notes"]
            self.eating_disorder_id: UUID = staged_client_json["eating_disorder_id"]
            # account info
            self.datetime: float = float(staged_client_json["datetime"])
            self.account_created: bool = staged_client_json["account_created"]
            self.active: bool = staged_client_json["active"]
            self.waitlisted: bool = staged_client_json["waitlisted"]
            self.meals_pre_selected: bool = staged_client_json["meals_pre_selected"]
            self.meals_prepaid: bool = staged_client_json["meals_prepaid"]
        elif staged_client_domain:
            self.id: str = staged_client_domain.id
            self.email: str = staged_client_domain.email
            self.dietitian_id: Optional[str] = staged_client_domain.dietitian_id
            self.meal_plan_id: UUID = staged_client_domain.meal_plan_id
            # personal info
            self.first_name: str = staged_client_domain.first_name
            self.current_weight: int = staged_client_domain.current_weight
            self.target_weight: float = staged_client_domain.target_weight
            self.age: str = staged_client_domain.age
            self.gender: str = staged_client_domain.gender
            self.notes: str = staged_client_domain.notes
            self.eating_disorder_id: UUID = staged_client_domain.eating_disorder_id
            # account info
            self.datetime: float = staged_client_domain.datetime
            self.account_created: bool = staged_client_domain.account_created
            self.active: bool = staged_client_domain.active
            self.waitlisted: bool = staged_client_domain.waitlisted
            self.meals_pre_selected: bool = staged_client_domain.meals_pre_selected
            self.meals_prepaid: bool = staged_client_domain.meals_prepaid
