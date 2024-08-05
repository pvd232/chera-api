from models import Staged_Schedule_Meal_Model
from .Base_Domain import Base_Domain
from typing import Optional


class Staged_Schedule_Meal_Domain(Base_Domain):
    def __init__(
        self,
        staged_schedule_meal_object: Optional[Staged_Schedule_Meal_Model] = None,
        staged_schedule_meal_json: Optional[dict] = None,
    ) -> None:
        if staged_schedule_meal_object:
            self.id = staged_schedule_meal_object.id
            self.meal_id = staged_schedule_meal_object.meal_id
            self.staged_client_id = staged_schedule_meal_object.staged_client_id
        elif staged_schedule_meal_json:
            self.id = staged_schedule_meal_json["id"]
            self.meal_id = staged_schedule_meal_json["meal_id"]
            self.staged_client_id = staged_schedule_meal_json["staged_client_id"]
