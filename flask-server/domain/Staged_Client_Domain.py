from models import Staged_Client_Model
from dto.Staged_Client_DTO import Staged_Client_DTO
from uuid import UUID
from .Base_Domain import Base_Domain


class Staged_Client_Domain(Base_Domain):
    def __init__(self, staged_client_object: Staged_Client_Model | Staged_Client_DTO) -> None:
        self.id: str = staged_client_object.id
        self.first_name: str = staged_client_object.first_name
        self.dietitian_id: str = staged_client_object.dietitian_id
        self.meal_plan_id: UUID = staged_client_object.meal_plan_id
        self.notes: str = staged_client_object.notes
        self.datetime: float = staged_client_object.datetime
        self.account_created: bool = staged_client_object.account_created
        self.active: bool = staged_client_object.active
        self.waitlisted: bool = staged_client_object.waitlisted
        self.meals_pre_selected: bool = staged_client_object.meals_pre_selected
        self.meals_prepaid: bool = staged_client_object.meals_prepaid
