from uuid import UUID
from .Base_Domain import Base_Domain
from models import COGS_Model
from dto.COGS_DTO import COGS_DTO


class COGS_Domain(Base_Domain):
    def __init__(self, cogs_object: COGS_Model | COGS_DTO) -> None:
        self.num_meals: int = cogs_object.num_meals
        self.is_local: bool = cogs_object.is_local
        self.ingredient: float = cogs_object.ingredient
        self.core_packaging: float = cogs_object.core_packaging
        self.kitchen: float = cogs_object.kitchen
        self.chef: float = cogs_object.chef
        self.box: float = cogs_object.box
        self.ice: float = cogs_object.ice
        self.num_boxes: int = cogs_object.num_boxes
