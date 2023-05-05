from uuid import UUID
from typing import TYPE_CHECKING
from .Base_DTO import Base_DTO
if TYPE_CHECKING:
    from domain.Dietitian_Domain import Dietitian_Domain


class Dietitian_DTO(Base_DTO):
    def __init__(self, dietitian_json: dict = None, dietitian_domain: 'Dietitian_Domain' = None) -> None:
        if dietitian_json:
            self.id: str = dietitian_json["id"]
            self.password: str = dietitian_json["password"]
            self.first_name: str = dietitian_json["first_name"]
            self.last_name: str = dietitian_json["last_name"]
            self.clinic_name: str = dietitian_json["clinic_name"]
            self.clinic_zipcode: str = dietitian_json["clinic_zipcode"]
            self.datetime: float = float(dietitian_json["datetime"])
            self.active: bool = dietitian_json["active"]
            if self.id == "patardriscoll@gmail.com":
                self.admin = True
            else:
                self.admin = False

        elif dietitian_domain:
            self.id: str = dietitian_domain.id
            self.password: str = dietitian_domain.password
            self.first_name: str = dietitian_domain.first_name
            self.last_name: str = dietitian_domain.last_name
            self.clinic_name: str = dietitian_domain.clinic_name
            self.clinic_zipcode: str = dietitian_domain.clinic_zipcode
            self.datetime: float = dietitian_domain.datetime
            self.active: bool = dietitian_domain.active
            if self.id == "patardriscoll@gmail.com":
                self.admin = True
            else:
                self.admin = False
