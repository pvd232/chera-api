from .Base_Domain import Base_Domain
from models import Discount_Model
from dto.Discount_DTO import Discount_DTO
from uuid import UUID


class Discount_Domain(Base_Domain):
    def __init__(self, discount_object: Discount_Model | Discount_DTO) -> None:
        if discount_object:
            self.id: UUID = discount_object.id
            self.code: str = discount_object.code
            self.discount_percentage: float = discount_object.discount_percentage
            self.active: bool = discount_object.active
