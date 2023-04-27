from domain.Schedule_Snack_Domain import Schedule_Snack_Domain
from uuid import UUID
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from repository.Schedule_Snack_Repository import Schedule_Snack_Repository
    from service.Client_Service import Client_Service
    from dto.Schedule_Snack_DTO import Schedule_Snack_DTO


class Schedule_Snack_Service(object):
    def __init__(self, schedule_snack_repository: "Schedule_Snack_Repository") -> None:
        self.schedule_snack_repository = schedule_snack_repository

    def create_schedule_snacks(
        self, schedule_snack_dtos: list["Schedule_Snack_DTO"]
    ) -> None:
        schedule_snack_domains: list[Schedule_Snack_Domain] = [
            Schedule_Snack_Domain(schedule_snack_object=x) for x in schedule_snack_dtos
        ]
        self.schedule_snack_repository.create_schedule_snacks(
            schedule_snack_domains=schedule_snack_domains
        )

    def get_schedule_snacks(
        self, meal_subscription_id: UUID = None
    ) -> Optional[list[Schedule_Snack_Domain]]:
        schedule_snack_models = self.schedule_snack_repository.get_schedule_snacks(
            meal_subscription_id=meal_subscription_id
        )
        if schedule_snack_models:
            return [
                Schedule_Snack_Domain(schedule_snack_object=x)
                for x in schedule_snack_models
            ]
        else:
            return None

    def get_dietitian_schedule_snacks(
        self, dietitian_id: list[str], client_service: "Client_Service"
    ) -> Optional[list[Schedule_Snack_Domain]]:
        dietitian_schedule_snack_models = (
            self.schedule_snack_repository.get_dietitian_schedule_snacks(
                dietitian_id=dietitian_id,
                client_repository=client_service.client_repository,
            )
        )
        if dietitian_schedule_snack_models:
            return [
                Schedule_Snack_Domain(schedule_snack_object=x)
                for x in dietitian_schedule_snack_models
            ]
        else:
            return None

    def delete_schedule_snacks(self, meal_subscription_id: UUID) -> None:
        return self.schedule_snack_repository.delete_schedule_snacks(
            meal_subscription_id=meal_subscription_id
        )
