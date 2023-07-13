from uuid import UUID
from typing import TYPE_CHECKING
from .Base_DTO import Base_DTO

if TYPE_CHECKING:
    from domain.Client_Domain import Client_Domain


class Client_DTO(Base_DTO):
    def __init__(
        self, client_json: dict = None, client_domain: "Client_Domain" = None
    ) -> None:
        if client_json:
            self.id: UUID = client_json["id"]
            self.dietitian_id: str = client_json["dietitian_id"]
            self.meal_plan_id: UUID = UUID(client_json["meal_plan_id"])
            self.stripe_id: str = client_json["stripe_id"]
            self.first_name: str = client_json["first_name"]
            self.last_name: str = client_json["last_name"]
            self.street: str = client_json["street"]
            self.suite: str = client_json["suite"]
            self.city: str = client_json["city"]
            self.state: str = client_json["state"]
            self.zipcode: str = client_json["zipcode"]
            self.zipcode_extension: str = client_json["zipcode_extension"]
            self.address: str = client_json["address"]
            self.notes: str = client_json["notes"]
            self.phone_number: str = client_json["phone_number"]

            self.datetime: float = float(client_json["datetime"])
            self.active: bool = client_json["active"]

        elif client_domain:
            self.id: str = client_domain.id
            self.dietitian_id: str = client_domain.dietitian_id
            self.meal_plan_id: UUID = client_domain.meal_plan_id
            self.stripe_id: str = client_domain.stripe_id
            self.first_name: str = client_domain.first_name
            self.last_name: str = client_domain.last_name
            self.street: str = client_domain.street
            self.suite: str = client_domain.suite
            self.city: str = client_domain.city
            self.state: str = client_domain.state
            self.zipcode: str = client_domain.zipcode
            self.zipcode_extension: str = client_domain.zipcode_extension
            self.address: str = client_domain.address
            self.phone_number: str = client_domain.phone_number
            self.notes: str = client_domain.notes
            self.datetime: float = client_domain.datetime
            self.active: bool = client_domain.active
