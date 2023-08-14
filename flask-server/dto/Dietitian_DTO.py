from uuid import UUID
from typing import TYPE_CHECKING
from .Base_DTO import Base_DTO

if TYPE_CHECKING:
    from domain.Dietitian_Domain import Dietitian_Domain
    from service.GCP_Secret_Manager_Service import GCP_Secret_Manager_Service


class Dietitian_DTO(Base_DTO):
    def __init__(
        self,
        dietitian_json: dict = None,
        dietitian_domain: "Dietitian_Domain" = None,
    ) -> None:
        if dietitian_json:
            self.id: UUID = dietitian_json["id"]
            self.email: str = dietitian_json["email"]
            self.phone_number: str = dietitian_json["phone_number"]
            self.first_name: str = dietitian_json["first_name"]
            self.last_name: str = dietitian_json["last_name"]
            self.dietetic_registration_number: str = dietitian_json[
                "dietetic_registration_number"
            ]
            self.clinic_city: str = dietitian_json["clinic_city"]
            self.clinic_state: str = dietitian_json["clinic_state"]
            self.clinic_address: str = dietitian_json["clinic_address"]
            self.number_of_ed_clients: int = dietitian_json["number_of_ed_clients"]
            self.datetime: float = float(dietitian_json["datetime"])
            self.got_sample: bool = dietitian_json["got_sample"]
            self.active: bool = dietitian_json["active"]

        elif dietitian_domain:
            self.id: UUID = dietitian_domain.id
            self.email: str = dietitian_domain.email
            self.phone_number: str = dietitian_domain.phone_number
            self.first_name: str = dietitian_domain.first_name
            self.last_name: str = dietitian_domain.last_name
            self.dietetic_registration_number: str = (
                dietitian_domain.dietetic_registration_number
            )
            self.clinic_city: str = dietitian_domain.clinic_city
            self.clinic_state: str = dietitian_domain.clinic_state
            self.clinic_address: str = dietitian_domain.clinic_address
            self.number_of_ed_clients: int = dietitian_domain.number_of_ed_clients
            self.datetime: float = dietitian_domain.datetime
            self.got_sample: bool = dietitian_domain.got_sample
            self.active: bool = dietitian_domain.active
