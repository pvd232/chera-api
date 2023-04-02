from repository.Base_Repository import Base_Repository
from models import Schedule_Meal_Model
from uuid import UUID
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from repository.Client_Repository import Client_Repository
    from domain.Schedule_Meal_Domain import Schedule_Meal_Domain


class Schedule_Meal_Repository(Base_Repository):
    def create_schedule_meals(self,  schedule_meal_domains: list['Schedule_Meal_Domain']) -> None:
        for schedule_meal_domain in schedule_meal_domains:
            new_schedule_meal = Schedule_Meal_Model(
                id=schedule_meal_domain.id, meal_id=schedule_meal_domain.meal_id, meal_subscription_id=schedule_meal_domain.meal_subscription_id)
            self.db.session.add(new_schedule_meal)
        self.db.session.commit()
        return

    def get_schedule_meals(self,  meal_subscription_id: UUID = None) -> Optional[list[Schedule_Meal_Model]]:
        if meal_subscription_id:
            schedule_meals: list[Schedule_Meal_Model] = self.db.session.query(Schedule_Meal_Model).filter(
                Schedule_Meal_Model.meal_subscription_id == meal_subscription_id).all()
        else:
            schedule_meals: list[Schedule_Meal_Model] = self.db.session.query(
                Schedule_Meal_Model).all()
        return schedule_meals

    def get_dietitian_schedule_meals(self,  dietitian_id: list[str], client_repository: 'Client_Repository') -> Optional[list[Schedule_Meal_Model]]:
        schedule_meals: list[Schedule_Meal_Model] = []
        meal_subscription_ids = []
        clients = client_repository.get_clients(
            dietitian_id=dietitian_id)
        for client in clients:
            for meal_subscription in client.meal_subscription:
                if meal_subscription.active == True:
                    meal_subscription_ids.append(meal_subscription.id)

        for meal_subscription_id in meal_subscription_ids:
            schedule_meals += self.get_schedule_meals(
                meal_subscription_id=meal_subscription_id)
        return schedule_meals

    def delete_schedule_meals(self,  meal_subscription_id: UUID) -> None:
        schedule_meals_to_delete: list[Schedule_Meal_Model] = self.db.session.query(
            Schedule_Meal_Model).filter(Schedule_Meal_Model.meal_subscription_id == meal_subscription_id)
        for schedule_meal in schedule_meals_to_delete:
            self.db.session.delete(schedule_meal)
        self.db.session.commit()
