from .Schedule_Snack_Service import Schedule_Snack_Service
from domain.Extended_Schedule_Snack_Domain import Extended_Schedule_Snack_Domain
from uuid import UUID
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from models import Schedule_Snack_Model
    from service.Client_Service import Client_Service


class Extended_Schedule_Snack_Service(Schedule_Snack_Service):
    def get_extended_schedule_snacks(
        self, meal_subscription_id: UUID
    ) -> Optional[list["Extended_Schedule_Snack_Domain"]]:
        schedule_snacks: Optional[
            list["Schedule_Snack_Model"]
        ] = self.schedule_snack_repository.get_schedule_snacks(
            meal_subscription_id=meal_subscription_id
        )
        if schedule_snacks:
            return [
                Extended_Schedule_Snack_Domain(schedule_snack_object=x)
                for x in schedule_snacks
            ]
        else:
            return None

    def get_dietitian_extended_schedule_snacks(
        self, dietitian_id: str, client_service: "Client_Service"
    ) -> Optional[list["Extended_Schedule_Snack_Domain"]]:
        schedule_snacks: Optional[
            list["Schedule_Snack_Model"]
        ] = self.schedule_snack_repository.get_dietitian_schedule_snacks(
            dietitian_id=dietitian_id,
            client_repository=client_service.client_repository,
        )
        if schedule_snacks:
            return [
                Extended_Schedule_Snack_Domain(schedule_snack_model=x)
                for x in schedule_snacks
            ]
        else:
            return None
