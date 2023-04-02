from models import Schedule_Meal_Model
from .Base_Domain import Base_Domain
from dto.Schedule_Meal_DTO import Schedule_Meal_DTO


class Schedule_Meal_Domain(Base_Domain):
    def __init__(self, schedule_meal_object: Schedule_Meal_Model | Schedule_Meal_DTO) -> None:
        self.id = schedule_meal_object.id
        self.meal_id = schedule_meal_object.meal_id
        self.meal_subscription_id = schedule_meal_object.meal_subscription_id
