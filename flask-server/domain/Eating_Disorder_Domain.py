from models import Eating_Disorder_Model
from dto.Eating_Disorder_DTO import Eating_Disorder_DTO
# from uuid import UUID
from .Base_Domain import Base_Domain


class Eating_Disorder_Domain(Base_Domain):
    def __init__(self, eating_disorder_object: Eating_Disorder_Model | Eating_Disorder_DTO) -> None:
        self.id: str = eating_disorder_object.id
        self.name: str = eating_disorder_object.name

