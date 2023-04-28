from models import Staged_Schedule_Snack_Model
from .Base_Domain import Base_Domain


class Staged_Schedule_Snack_Domain(Base_Domain):
    def __init__(
        self,
        staged_schedule_snack_object: Staged_Schedule_Snack_Model = None,
        staged_schedule_snack_json: dict = None,
    ) -> None:
        if staged_schedule_snack_object:
            self.id = staged_schedule_snack_object.id
            self.snack_id = staged_schedule_snack_object.snack_id
            self.staged_client_id = staged_schedule_snack_object.staged_client_id
        elif staged_schedule_snack_json:
            self.id = staged_schedule_snack_json["id"]
            self.snack_id = staged_schedule_snack_json["snack_id"]
            self.staged_client_id = staged_schedule_snack_json["staged_client_id"]
