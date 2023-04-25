from repository.Base_Repository import Base_Repository
from models import Scheduled_Order_Meal_Model
from uuid import UUID
from datetime import datetime, timedelta, timezone
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from domain.Scheduled_Order_Meal_Domain import Scheduled_Order_Meal_Domain


class Scheduled_Order_Meal_Repository(Base_Repository):
    def get_upcoming_scheduled_order_meals(self,  meal_subscription_id: UUID) -> Optional[list[Scheduled_Order_Meal_Model]]:
        scheduled_order_meals = self.db.session.query(Scheduled_Order_Meal_Model).filter(
            Scheduled_Order_Meal_Model.meal_subscription_id == meal_subscription_id, Scheduled_Order_Meal_Model.delivery_date > datetime.now(timezone.utc).timestamp()).all()
        if scheduled_order_meals:
            return scheduled_order_meals
        else:
            return None

    def get_scheduled_order_meals(self,  meal_subscription_id: UUID = None) -> Optional[list[Scheduled_Order_Meal_Model]]:
        if meal_subscription_id:
            scheduled_order_meals: Optional[list[Scheduled_Order_Meal_Model]] = self.db.session.query(
                Scheduled_Order_Meal_Model).filter(Scheduled_Order_Meal_Model.meal_subscription_id == meal_subscription_id)
            if scheduled_order_meals:
                return scheduled_order_meals
            else:
                return False
        else:
            scheduled_order_meals: Optional[list[Scheduled_Order_Meal_Model]] = self.db.session.query(
                Scheduled_Order_Meal_Model).all()
        return scheduled_order_meals

    def get_scheduled_order_meals_for_week(self,  meal_subscription_id: UUID, delivery_date: float) -> Optional[list[Scheduled_Order_Meal_Model]]:
        weekly_scheduled_order_meals = self.db.session.query(Scheduled_Order_Meal_Model).filter(
            Scheduled_Order_Meal_Model.meal_subscription_id == meal_subscription_id, Scheduled_Order_Meal_Model.delivery_date == delivery_date).all()
        return weekly_scheduled_order_meals

    def create_scheduled_order_meal(self,  scheduled_order_meal: 'Scheduled_Order_Meal_Domain') -> None:
        new_scheduled_order_meal = Scheduled_Order_Meal_Model(
            scheduled_order_meal_domain=scheduled_order_meal)
        self.db.session.add(new_scheduled_order_meal)
        self.db.session.commit()

        return

    def create_scheduled_order_meals(self,  scheduled_order_meal_domains: list['Scheduled_Order_Meal_Domain']) -> None:
        for scheduled_order_meal_domain in scheduled_order_meal_domains:
            new_scheduled_order_meal = Scheduled_Order_Meal_Model(
                scheduled_order_meal_domain=scheduled_order_meal_domain)
            self.db.session.add(new_scheduled_order_meal)
        self.db.session.commit()

        return

    def update_home_page_scheduled_order_meals(self, meal_subscription_id: UUID, updated_scheduled_order_meals: list['Scheduled_Order_Meal_Domain']) -> None:
        current_scheduled_order_meals = self.get_upcoming_scheduled_order_meals(
            meal_subscription_id=meal_subscription_id)
        current_scheduled_order_meals_map = {}

        # Create a map of the current scheduled order meals
        for current_scheduled_order_meal in current_scheduled_order_meals:
            current_scheduled_order_meals_map[str(
                current_scheduled_order_meal.id)] = ""

        for updated_scheduled_order_meal in updated_scheduled_order_meals:
            # If the updated scheduled order meal is not in the current scheduled order meals map, then it is a new scheduled order meal
            if str(updated_scheduled_order_meal.id) not in current_scheduled_order_meals_map:
                new_scheduled_order_meal = Scheduled_Order_Meal_Model(
                    scheduled_order_meal_domain=updated_scheduled_order_meal)
                self.db.session.add(new_scheduled_order_meal)
            # Otherwise, it is an unchanged existing scheduled order meal and is removed from the current scheduled order meals map
            else:
                current_scheduled_order_meals_map.pop(
                    str(updated_scheduled_order_meal.id))

        # All remaining scheduled order meals in the current scheduled order meals map are scheduled order meals that have been removed
        for scheduled_order_meal_id in current_scheduled_order_meals_map.keys():
            scheduled_order_meal_to_delete = self.db.session.query(Scheduled_Order_Meal_Model).filter(
                Scheduled_Order_Meal_Model.id == UUID(scheduled_order_meal_id)).first()
            self.db.session.delete(scheduled_order_meal_to_delete)
        self.db.session.commit()
        return

    def skip_weekly_scheduled_order_meals(self,  meal_subscription_id: UUID, delivery_date: float) -> None:
        weekly_scheduled_order_meals = self.db.session.query(Scheduled_Order_Meal_Model).filter(
            Scheduled_Order_Meal_Model.meal_subscription_id == meal_subscription_id, Scheduled_Order_Meal_Model.delivery_date == delivery_date).all()
        for scheduled_order_meal in weekly_scheduled_order_meals:
            scheduled_order_meal.delivery_skipped = True
        self.db.session.commit()
        return

    def unskip_weekly_scheduled_order_meals(self,  meal_subscription_id: UUID, delivery_date: float) -> None:
        weekly_scheduled_order_meals = self.db.session.query(Scheduled_Order_Meal_Model).filter(
            Scheduled_Order_Meal_Model.meal_subscription_id == meal_subscription_id, Scheduled_Order_Meal_Model.delivery_date == delivery_date).all()
        for scheduled_order_meal in weekly_scheduled_order_meals:
            scheduled_order_meal.delivery_skipped = False
        self.db.session.commit()
        return

    def update_scheduled_order_meals(self,  scheduled_order_meals: list['Scheduled_Order_Meal_Domain']) -> None:
        for scheduled_order_meal in scheduled_order_meals:
            scheduled_order_meal_to_update: Scheduled_Order_Meal_Model = self.db.session.query(Scheduled_Order_Meal_Model).filter(
                Scheduled_Order_Meal_Model.id == scheduled_order_meal.id).first()
            scheduled_order_meal_to_update.delivery_skipped = scheduled_order_meal.delivery_skipped
        self.db.session.commit()

        return

    def pause_scheduled_order_meals(self,  meal_subscription_id: UUID) -> None:
        scheduled_order_meals_to_pause = self.get_upcoming_scheduled_order_meals(
            meal_subscription_id=meal_subscription_id)
        for scheduled_order_meal in scheduled_order_meals_to_pause:
            if self.can_pause_scheduled_order_meal(scheduled_order_meal=scheduled_order_meal):
                scheduled_order_meal.paused = True
        self.db.session.commit()
        return

    def unpause_scheduled_order_meals(self,  meal_subscription_id: UUID) -> None:
        scheduled_order_meals_to_unpause = self.get_upcoming_scheduled_order_meals(
            meal_subscription_id=meal_subscription_id)
        for scheduled_order_meal in scheduled_order_meals_to_unpause:
            scheduled_order_meal.paused = False
        self.db.session.commit()
        return

    def delete_scheduled_order_meals(self,  meal_subscription_id: UUID, cutoff_date: float, current_week_delivery_date: float, is_first_week: bool) -> None:
        scheduled_order_meals_to_delete = self.get_upcoming_scheduled_order_meals(
            meal_subscription_id=meal_subscription_id)
        today = datetime.now(timezone.utc).timestamp()
        for scheduled_order_meal in scheduled_order_meals_to_delete:
            # Only delete the current week scheduled order meals if its before the cutoff date and it isnt the first week of the subscription
            if today < cutoff_date and not is_first_week:
                self.db.session.delete(scheduled_order_meal)
            else:
                if scheduled_order_meal.delivery_date > current_week_delivery_date:
                    self.db.session.delete(scheduled_order_meal)
            self.db.session.commit()
        return

    def can_pause_scheduled_order_meal(self, scheduled_order_meal: 'Scheduled_Order_Meal_Domain') -> bool:
        if datetime.utcfromtimestamp(scheduled_order_meal.delivery_date).replace(tzinfo=timezone.utc) - datetime.now(timezone.utc) > timedelta(days=2):
            return True
        else:
            return False
