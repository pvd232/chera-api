from models import Dietitian_Model
from .Base_Domain import Base_Domain
from dto.Dietitian_DTO import Dietitian_DTO
from datetime import datetime


class Dietitian_Domain(Base_Domain):
    def __init__(self, dietitian_object: Dietitian_Model | Dietitian_DTO) -> None:
        self.id: str = dietitian_object.id
        self.password: str = dietitian_object.password
        self.first_name: str = dietitian_object.first_name
        self.last_name: str = dietitian_object.last_name
        self.clinic_name: str = dietitian_object.clinic_name
        self.clinic_zipcode: str = dietitian_object.clinic_zipcode
        self.datetime: float = dietitian_object.datetime
        self.active: bool = dietitian_object.active
