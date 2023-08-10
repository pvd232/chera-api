from models import Meal_Sample_Model
from .Base_Domain import Base_Domain
from dto.Meal_Sample_DTO import Meal_Sample_DTO
from uuid import UUID


class Meal_Sample_Domain(Base_Domain):
    def __init__(self, meal_sample_object: Meal_Sample_Model | Meal_Sample_DTO) -> None:
        self.id: UUID = meal_sample_object.id
        self.meal_id: UUID = meal_sample_object.meal_id
        self.dietitian_id: UUID = meal_sample_object.dietitian_id
