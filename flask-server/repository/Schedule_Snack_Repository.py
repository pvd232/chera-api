from repository.Base_Repository import Base_Repository
from models import Schedule_Snack_Model
from uuid import UUID
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from repository.Client_Repository import Client_Repository
    from domain.Schedule_Snack_Domain import Schedule_Snack_Domain


class Schedule_Snack_Repository(Base_Repository):
    def create_schedule_snacks(
        self, schedule_snack_domains: list["Schedule_Snack_Domain"]
    ) -> None:
        for schedule_snack_domain in schedule_snack_domains:
            new_schedule_snack = Schedule_Snack_Model(
                id=schedule_snack_domain.id,
                snack_id=schedule_snack_domain.snack_id,
                meal_subscription_id=schedule_snack_domain.meal_subscription_id,
            )
            self.db.session.add(new_schedule_snack)
        self.db.session.commit()
        return

    def get_schedule_snacks(
        self, meal_subscription_id: Optional[UUID] = None
    ) -> Optional[list[Schedule_Snack_Model]]:
        if meal_subscription_id:
            schedule_snacks: list[Schedule_Snack_Model] = (
                self.db.session.query(Schedule_Snack_Model)
                .filter(
                    Schedule_Snack_Model.meal_subscription_id == meal_subscription_id
                )
                .all()
            )
        else:
            schedule_snacks: list[Schedule_Snack_Model] = self.db.session.query(
                Schedule_Snack_Model
            ).all()
        return schedule_snacks

    def get_dietitian_schedule_snacks(
        self, dietitian_id: list[str], client_repository: "Client_Repository"
    ) -> Optional[list[Schedule_Snack_Model]]:
        schedule_snacks: list[Schedule_Snack_Model] = []
        meal_subscription_ids = []
        clients = client_repository.get_clients(dietitian_id=dietitian_id)
        for client in clients:
            for meal_subscription in client.meal_subscription:
                if meal_subscription.active == True:
                    meal_subscription_ids.append(meal_subscription.id)

        for meal_subscription_id in meal_subscription_ids:
            schedule_snacks += self.get_schedule_snacks(
                meal_subscription_id=meal_subscription_id
            )
        return schedule_snacks

    def delete_schedule_snacks(self, meal_subscription_id: UUID) -> None:
        schedule_snacks_to_delete: list[Schedule_Snack_Model] = self.db.session.query(
            Schedule_Snack_Model
        ).filter(Schedule_Snack_Model.meal_subscription_id == meal_subscription_id)
        for schedule_snack in schedule_snacks_to_delete:
            self.db.session.delete(schedule_snack)
        self.db.session.commit()
