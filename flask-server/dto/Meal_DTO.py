from uuid import UUID
from typing import TYPE_CHECKING
from .Base_DTO import Base_DTO
if TYPE_CHECKING:
    from domain.Meal_Domain import Meal_Domain


class Meal_DTO(Base_DTO):
    def __init__(self, meal_json: dict = None, meal_domain: 'Meal_Domain' = None) -> None:
        if meal_json:
            self.id: UUID = UUID(meal_json["id"])
            self.meal_time: str = meal_json["meal_time"]
            self.name: str = meal_json["name"]
            self.description: str = meal_json["description"]
            self.image_url: str = meal_json["image_url"]
            self.active: bool = meal_json["active"]

        elif meal_domain:
            self.id: UUID = meal_domain.id
            self.meal_time: str = meal_domain.meal_time
            self.name: str = meal_domain.name
            self.description: str = meal_domain.description
            self.image_url: str = meal_domain.image_url
            self.active: bool = meal_domain.active
