from typing import TYPE_CHECKING
from .Base_DTO import Base_DTO

if TYPE_CHECKING:
    from domain.Dietitian_Domain import Dietitian_Domain
    from service.GCP_Secret_Manager_Service import GCP_Secret_Manager_Service


class Dietitian_DTO(Base_DTO):
    def __init__(
        self,
        gcp_secret_manager_service: "GCP_Secret_Manager_Service",
        dietitian_json: dict = None,
        dietitian_domain: "Dietitian_Domain" = None,
    ) -> None:
        if dietitian_json:
            self.id: str = dietitian_json["id"]
            self.password: str = dietitian_json["password"]
            self.first_name: str = dietitian_json["first_name"]
            self.last_name: str = dietitian_json["last_name"]
            self.dietetic_registration_number: str = dietitian_json[
                "dietetic_registration_number"
            ]
            self.clinic_city: str = dietitian_json["clinic_city"]
            self.clinic_state: str = dietitian_json["clinic_state"]
            self.clinic_address: str = dietitian_json["clinic_address"]
            self.clinic_url: str = dietitian_json["clinic_url"]
            self.datetime: float = float(dietitian_json["datetime"])
            self.got_sample: bool = dietitian_json["got_sample"]
            self.active: bool = dietitian_json["active"]

            if self.id == gcp_secret_manager_service.get_secret("ADMIN_ID"):
                self.admin = True
            else:
                self.admin = False

        elif dietitian_domain:
            self.id: str = dietitian_domain.id
            self.password: str = dietitian_domain.password
            self.first_name: str = dietitian_domain.first_name
            self.last_name: str = dietitian_domain.last_name
            self.dietetic_registration_number: str = (
                dietitian_domain.dietetic_registration_number
            )
            self.clinic_city: str = dietitian_domain.clinic_city
            self.clinic_state: str = dietitian_domain.clinic_state
            self.clinic_address: str = dietitian_domain.clinic_address
            self.clinic_url: str = dietitian_domain.clinic_url
            self.datetime: float = dietitian_domain.datetime
            self.got_sample: bool = dietitian_domain.got_sample
            self.active: bool = dietitian_domain.active
            if self.id == "patardriscoll@gmail.com":
                self.admin = True
            else:
                self.admin = False
