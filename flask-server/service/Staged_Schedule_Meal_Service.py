from domain.Staged_Schedule_Meal_Domain import Staged_Schedule_Meal_Domain
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from repository.Staged_Schedule_Meal_Repository import Staged_Schedule_Meal_Repository
    from dto.Staged_Schedule_Meal_DTO import Staged_Schedule_Meal_DTO


class Staged_Schedule_Meal_Service(object):
    def __init__(self, staged_schedule_meal_repository: 'Staged_Schedule_Meal_Repository') -> None:
        self.staged_schedule_meal_repository = staged_schedule_meal_repository

    def create_staged_schedule_meals(self, staged_schedule_meal_dtos: list['Staged_Schedule_Meal_DTO']) -> None:
        staged_schedule_meal_domains: list[Staged_Schedule_Meal_Domain] = [Staged_Schedule_Meal_Domain(
            staged_schedule_meal_object=x) for x in staged_schedule_meal_dtos]
        self.staged_schedule_meal_repository.create_staged_schedule_meals(
            staged_schedule_meal_domains=staged_schedule_meal_domains)

    def get_staged_schedule_meals(self, staged_client_id: str) -> Optional[list[Staged_Schedule_Meal_Domain]]:
        staged_schedule_meal_models = self.staged_schedule_meal_repository.get_staged_schedule_meals(
            staged_client_id=staged_client_id)
        if staged_schedule_meal_models:
            staged_schedule_meal_domains: list[Staged_Schedule_Meal_Domain] = [Staged_Schedule_Meal_Domain(
                staged_schedule_meal_object=x) for x in staged_schedule_meal_models]
        return staged_schedule_meal_domains
