from uuid import UUID
from typing import TYPE_CHECKING
from .Base_DTO import Base_DTO
if TYPE_CHECKING:
    from domain.Eating_Disorder_Domain import Eating_Disorder_Domain


class Eating_Disorder_DTO(Base_DTO):
    def __init__(self, eating_disorder_json: dict = None, eating_disorder_domain: 'Eating_Disorder_Domain' = None) -> None:
        if eating_disorder_json:
            self.id: str = eating_disorder_json["id"]
            self.name: str = eating_disorder_json["name"]

        elif eating_disorder_domain:
            self.id: str = eating_disorder_domain.id
            self.name: str = eating_disorder_domain.name

