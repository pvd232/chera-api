from .Base_Domain import Base_Domain
from models import Imperial_Unit_Model
from dto.Imperial_Unit_DTO import Imperial_Unit_DTO


class Imperial_Unit_Domain(Base_Domain):
    def __init__(
        self, imperial_unit_object: Imperial_Unit_Model | Imperial_Unit_DTO
    ) -> None:
        self.id: str = imperial_unit_object.id
        self.ounces: float = imperial_unit_object.ounces
