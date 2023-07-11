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
        self.dietetic_registration_number: str = (
            dietitian_object.dietetic_registration_number
        )
        self.clinic_city: str = dietitian_object.clinic_city
        self.clinic_state: str = dietitian_object.clinic_state
        self.clinic_address: str = dietitian_object.clinic_address
        self.clinic_url: str = dietitian_object.clinic_url
        self.datetime: float = dietitian_object.datetime
        self.active: bool = dietitian_object.active
        self.got_sample: bool = dietitian_object.got_sample
