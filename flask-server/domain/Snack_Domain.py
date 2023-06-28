from .Base_Domain import Base_Domain
from models import Snack_Model
from dto.Snack_DTO import Snack_DTO


class Snack_Domain(Base_Domain):
    def __init__(self, snack_object: Snack_Model | Snack_DTO) -> None:
        self.id = snack_object.id
        self.name = snack_object.name
        self.description = snack_object.description
        self.image_url = snack_object.image_url
        self.active = snack_object.active
