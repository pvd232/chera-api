from domain.Meal_Dietary_Restriction_Domain import Meal_Dietary_Restriction_Domain
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from repository.Meal_Dietary_Restriction_Repository import Meal_Dietary_Restriction_Repository
    from dto.Meal_Dietary_Restriction_DTO import Meal_Dietary_Restriction_DTO


class Meal_Dietary_Restriction_Service(object):
    def __init__(self, meal_dietary_restriction_repository: 'Meal_Dietary_Restriction_Repository') -> None:
        self.meal_dietary_restriction_repository = meal_dietary_restriction_repository

    def create_meal_dietary_restriction(self, meal_dietary_restriction_dto: 'Meal_Dietary_Restriction_DTO') -> None:
        new_meal_dietary_restriction = Meal_Dietary_Restriction_Domain(
            meal_dietary_restriction_object=meal_dietary_restriction_dto)
        self.meal_dietary_restriction_repository.create_meal_dietary_restriction(
            meal_dietary_restriction_domain=new_meal_dietary_restriction)
        return
