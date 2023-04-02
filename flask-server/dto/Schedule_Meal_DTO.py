from .Base_DTO import Base_DTO
from uuid import UUID
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from domain.Schedule_Meal_Domain import Schedule_Meal_Domain


class Schedule_Meal_DTO(Base_DTO):
    def __init__(self, schedule_meal_domain: 'Schedule_Meal_Domain' = None, schedule_meal_json: dict = None) -> None:
        if schedule_meal_json:
            self.id: UUID = UUID(schedule_meal_json["id"])
            self.meal_id: UUID = UUID(schedule_meal_json["meal_id"])
            self.meal_subscription_id: UUID = UUID(
                schedule_meal_json["meal_subscription_id"])
        if schedule_meal_domain:
            self.id: UUID = schedule_meal_domain.id
            self.meal_id: UUID = schedule_meal_domain.meal_id
            self.meal_subscription_id: UUID = schedule_meal_domain.meal_subscription_id
