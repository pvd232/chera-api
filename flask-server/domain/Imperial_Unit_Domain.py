from .Base_Domain import Base_Domain
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models import Imperial_Unit_Model


class Imperial_Unit_Domain(Base_Domain):
    def __init__(self, imperial_unit_object: 'Imperial_Unit_Model') -> None:
        self.id = imperial_unit_object.id
        self.ounces = imperial_unit_object.ounces
