from models import Schedule_Snack_Model
from .Base_Domain import Base_Domain
from dto.Schedule_Snack_DTO import Schedule_Snack_DTO


class Schedule_Snack_Domain(Base_Domain):
    def __init__(
        self, schedule_snack_object: Schedule_Snack_Model | Schedule_Snack_DTO
    ) -> None:
        self.id = schedule_snack_object.id
        self.snack_id = schedule_snack_object.snack_id
        self.meal_subscription_id = schedule_snack_object.meal_subscription_id
