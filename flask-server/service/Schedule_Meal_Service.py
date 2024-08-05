from domain.Schedule_Meal_Domain import Schedule_Meal_Domain
from uuid import UUID
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from repository.Schedule_Meal_Repository import Schedule_Meal_Repository
    from service.Client_Service import Client_Service
    from dto.Schedule_Meal_DTO import Schedule_Meal_DTO


class Schedule_Meal_Service(object):
    def __init__(self, schedule_meal_repository: "Schedule_Meal_Repository") -> None:
        self.schedule_meal_repository = schedule_meal_repository

    def create_schedule_meals(
        self, schedule_meal_dtos: list["Schedule_Meal_DTO"]
    ) -> None:
        schedule_meal_domains: list[Schedule_Meal_Domain] = [
            Schedule_Meal_Domain(schedule_meal_object=x) for x in schedule_meal_dtos
        ]
        self.schedule_meal_repository.create_schedule_meals(
            schedule_meal_domains=schedule_meal_domains
        )

    def get_schedule_meals(
        self, meal_subscription_id: Optional[UUID] = None
    ) -> Optional[list[Schedule_Meal_Domain]]:
        schedule_meal_models = self.schedule_meal_repository.get_schedule_meals(
            meal_subscription_id=meal_subscription_id
        )
        if schedule_meal_models:
            return [
                Schedule_Meal_Domain(schedule_meal_object=x)
                for x in schedule_meal_models
            ]
        else:
            return None

    def get_dietitian_schedule_meals(
        self, dietitian_id: list[str], client_service: "Client_Service"
    ) -> Optional[list[Schedule_Meal_Domain]]:
        dietitian_schedule_meal_models = (
            self.schedule_meal_repository.get_dietitian_schedule_meals(
                dietitian_id=dietitian_id,
                client_repository=client_service.client_repository,
            )
        )
        if dietitian_schedule_meal_models:
            return [
                Schedule_Meal_Domain(schedule_meal_object=x)
                for x in dietitian_schedule_meal_models
            ]
        else:
            return None

    def delete_schedule_meals(self, meal_subscription_id: UUID) -> None:
        return self.schedule_meal_repository.delete_schedule_meals(
            meal_subscription_id=meal_subscription_id
        )
