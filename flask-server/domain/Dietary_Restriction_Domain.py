from domain.Base_Domain import Base_Domain
from models import Dietary_Restriction_Model
from dto.Dietary_Restriction_DTO import Dietary_Restriction_DTO


class Dietary_Restriction_Domain(Base_Domain):
    def __init__(self, dietary_restriction_object: Dietary_Restriction_Model | Dietary_Restriction_DTO) -> None:
        self.id = dietary_restriction_object.id
