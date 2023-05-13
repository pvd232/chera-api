from uuid import UUID
from datetime import datetime
from .Base_Domain import Base_Domain
from models import Client_Model
from dto.Client_DTO import Client_DTO


class Client_Domain(Base_Domain):
    def __init__(self, client_object: Client_Model | Client_DTO) -> None:
        self.id: str = client_object.id
        self.password: str = client_object.password
        self.dietitian_id: str = client_object.dietitian_id
        self.meal_plan_id: UUID = client_object.meal_plan_id
        self.stripe_id: str = client_object.stripe_id
        self.first_name: str = client_object.first_name
        self.last_name: str = client_object.last_name
        self.street: str = client_object.street
        self.suite: str = client_object.suite
        self.city: str = client_object.city
        self.state: str = client_object.state
        self.zipcode: int = client_object.zipcode
        self.zipcode_extension: int = client_object.zipcode_extension
        self.address: str = client_object.address
        self.phone_number: int = client_object.phone_number
        self.notes: str = client_object.notes
        self.datetime: float = client_object.datetime
        self.active: bool = client_object.active
