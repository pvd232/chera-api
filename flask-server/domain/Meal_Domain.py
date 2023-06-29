from .Base_Domain import Base_Domain
from models import Meal_Model
from dto.Meal_DTO import Meal_DTO


class Meal_Domain(Base_Domain):
    def __init__(self, meal_object: Meal_Model | Meal_DTO) -> None:
        self.id = meal_object.id
        self.meal_time = meal_object.meal_time
        self.name = meal_object.name
        self.description = meal_object.description
        self.image_url = meal_object.image_url
        self.active = meal_object.active
