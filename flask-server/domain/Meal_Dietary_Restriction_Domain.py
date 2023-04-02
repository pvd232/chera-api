from models import Meal_Dietary_Restriction_Model
from .Base_Domain import Base_Domain
from dto.Meal_Dietary_Restriction_DTO import Meal_Dietary_Restriction_DTO


class Meal_Dietary_Restriction_Domain(Base_Domain):
    def __init__(self, meal_dietary_restriction_object: Meal_Dietary_Restriction_Model | Meal_Dietary_Restriction_DTO) -> None:
        self.id = meal_dietary_restriction_object.id
        self.meal_id = meal_dietary_restriction_object.meal_id
        self.dietary_restriction_id = meal_dietary_restriction_object.dietary_restriction_id
