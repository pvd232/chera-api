from .Base_Domain import Base_Domain
from models import Discount_Model
from dto.Discount_DTO import Discount_DTO


class Discount_Domain(Base_Domain):
    def __init__(self, discount_object: Discount_Model = None | Discount_DTO) -> None:
        if discount_object:
            self.id = discount_object.id
            self.code = discount_object.code
            self.discount_percentage = discount_object.discount_percentage
            self.active = discount_object.active
