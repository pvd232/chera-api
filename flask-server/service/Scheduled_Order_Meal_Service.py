from domain.Scheduled_Order_Meal_Domain import Scheduled_Order_Meal_Domain
from datetime import datetime, timezone
from uuid import UUID, uuid4
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from models import Scheduled_Order_Meal_Model
    from repository.Scheduled_Order_Meal_Repository import (
        Scheduled_Order_Meal_Repository,
    )
    from service.Schedule_Meal_Service import Schedule_Meal_Service
    from service.Date_Service import Date_Service
    from dto.Scheduled_Order_Meal_DTO import Scheduled_Order_Meal_DTO


class Scheduled_Order_Meal_Service(object):
    def __init__(
        self, scheduled_order_meal_repository: "Scheduled_Order_Meal_Repository"
    ) -> None:
        self.scheduled_order_meal_repository = scheduled_order_meal_repository

    def update_scheduled_order_meals(
        self, scheduled_order_meal_dtos: list["Scheduled_Order_Meal_DTO"]
    ) -> None:
        scheduled_order_meal_domains = [
            Scheduled_Order_Meal_Domain(
                scheduled_order_meal_object=x,
                schedule_meal_object=None,
                scheduled_order_meal_id=None,
                delivery_date=None,
                is_paused=None,
            )
            for x in scheduled_order_meal_dtos
        ]
        self.scheduled_order_meal_repository.update_scheduled_order_meals(
            scheduled_order_meals=scheduled_order_meal_domains
        )
        return

    def skip_weekly_scheduled_order_meals(
        self, meal_subscription_id: UUID, delivery_date: float
    ) -> None:
        self.scheduled_order_meal_repository.skip_weekly_scheduled_order_meals(
            meal_subscription_id=meal_subscription_id, delivery_date=delivery_date
        )
        return

    def unskip_weekly_scheduled_order_meals(
        self, meal_subscription_id: UUID, delivery_date: float
    ) -> None:
        self.scheduled_order_meal_repository.unskip_weekly_scheduled_order_meals(
            meal_subscription_id=meal_subscription_id, delivery_date=delivery_date
        )
        return

    def update_home_page_scheduled_order_meals(
        self, scheduled_order_meal_dtos: list["Scheduled_Order_Meal_DTO"]
    ) -> None:
        scheduled_order_meal_domains = [
            Scheduled_Order_Meal_Domain(
                scheduled_order_meal_object=x,
                schedule_meal_object=None,
                scheduled_order_meal_id=None,
                delivery_date=None,
                is_paused=None,
            )
            for x in scheduled_order_meal_dtos
        ]
        self.scheduled_order_meal_repository.update_home_page_scheduled_order_meals(
            meal_subscription_id=scheduled_order_meal_domains[0].meal_subscription_id,
            updated_scheduled_order_meals=scheduled_order_meal_domains,
        )
        return

    def unpause_scheduled_order_meals(self, meal_subscription_id: UUID) -> None:
        self.scheduled_order_meal_repository.unpause_scheduled_order_meals(
            meal_subscription_id=meal_subscription_id
        )
        return

    def pause_scheduled_order_meals(self, meal_subscription_id: UUID) -> None:
        self.scheduled_order_meal_repository.pause_scheduled_order_meals(
            meal_subscription_id=meal_subscription_id
        )
        return

    # Delete all scheduled order meals for a meal subscription when client changes weekly meals
    def delete_scheduled_order_meals(
        self,
        meal_subscription_id: UUID,
        cutoff_date: float,
        current_week_delivery_date: float,
        is_first_week: bool,
    ) -> None:
        self.scheduled_order_meal_repository.delete_scheduled_order_meals(
            meal_subscription_id=meal_subscription_id,
            cutoff_date=cutoff_date,
            current_week_delivery_date=current_week_delivery_date,
            is_first_week=is_first_week,
        )
        return

    def create_scheduled_order_meal(
        self, scheduled_order_meal: Scheduled_Order_Meal_Domain
    ) -> None:
        self.scheduled_order_meal_repository.create_scheduled_order_meals(
            scheduled_order_meal_domain=scheduled_order_meal
        )

    def create_scheduled_order_meals(
        self, scheduled_order_meal_dtos: list["Scheduled_Order_Meal_DTO"]
    ) -> None:
        scheduled_order_meal_domains = [
            Scheduled_Order_Meal_Domain(
                scheduled_order_meal_object=x,
                schedule_meal_object=None,
                scheduled_order_meal_id=None,
                delivery_date=None,
                is_paused=None,
            )
            for x in scheduled_order_meal_dtos
        ]
        self.scheduled_order_meal_repository.create_scheduled_order_meals(
            scheduled_order_meal_domains=scheduled_order_meal_domains
        )
        return

    def get_upcoming_scheduled_order_meals(
        self, meal_subscription_id: UUID
    ) -> Optional[list[Scheduled_Order_Meal_Domain]]:
        scheduled_order_meals: Optional[
            list["Scheduled_Order_Meal_Model"]
        ] = self.scheduled_order_meal_repository.get_scheduled_order_meals(
            meal_subscription_id=meal_subscription_id
        )
        if scheduled_order_meals:
            return [
                Scheduled_Order_Meal_Domain(
                    scheduled_order_meal_object=x,
                    schedule_meal_object=None,
                    scheduled_order_meal_id=None,
                    delivery_date=None,
                    is_paused=None,
                )
                for x in scheduled_order_meals
            ]
        else:
            return None

    def get_scheduled_order_meals(
        self, meal_subscription_id: Optional[UUID]
    ) -> Optional[list[Scheduled_Order_Meal_Domain]]:
        scheduled_order_meals: Optional[
            list["Scheduled_Order_Meal_Model"]
        ] = self.scheduled_order_meal_repository.get_scheduled_order_meals(
            meal_subscription_id=meal_subscription_id
        )
        if scheduled_order_meals:
            return [
                Scheduled_Order_Meal_Domain(
                    scheduled_order_meal_object=x,
                    schedule_meal_object=None,
                    scheduled_order_meal_id=None,
                    delivery_date=None,
                    is_paused=None,
                )
                for x in scheduled_order_meals
            ]
        else:
            return None

    def get_scheduled_order_meals_for_week(
        self, meal_subscription_id: UUID, delivery_date: float
    ) -> Optional[list[Scheduled_Order_Meal_Domain]]:
        weekly_scheduled_order_meal_models = (
            self.scheduled_order_meal_repository.get_scheduled_order_meals_for_week(
                meal_subscription_id=meal_subscription_id, delivery_date=delivery_date
            )
        )
        if weekly_scheduled_order_meal_models:
            weekly_scheduled_order_meal_domains: list[Scheduled_Order_Meal_Domain] = [
                Scheduled_Order_Meal_Domain(
                    scheduled_order_meal_object=x,
                    schedule_meal_object=None,
                    scheduled_order_meal_id=None,
                    delivery_date=None,
                    is_paused=None,
                )
                for x in weekly_scheduled_order_meal_models
            ]
            return weekly_scheduled_order_meal_domains
        else:
            return None

    def get_current_scheduled_order_meal_delivery_dates(
        self, meal_subscription_id: UUID
    ) -> Optional[list[float]]:
        scheduled_order_meals: Optional[
            list[Scheduled_Order_Meal_Domain]
        ] = self.get_scheduled_order_meals(meal_subscription_id=meal_subscription_id)
        if scheduled_order_meals:
            date_dict = {}
            for meal in scheduled_order_meals:
                # Check if delivery date is in the future and not already in the dictionary
                if (
                    meal.delivery_date > datetime.now(timezone.utc).timestamp()
                    and meal.delivery_date not in date_dict
                ):
                    date_dict[meal.delivery_date] = ""
            date_list = list(date_dict.keys())
            date_list.sort()
            return date_list
        else:
            return None

    # Create new scheduled order meals on weekly basis when stripe generates invoice
    def refresh_scheduled_order_meals(
        self,
        meal_subscription_id: UUID,
        schedule_meal_service: "Schedule_Meal_Service",
        date_service: "Date_Service",
        is_paused: bool,
    ) -> None:
        delivery_dates = date_service.get_upcoming_delivery_dates()
        # If there are only 4 upcoming delivery dates then add the 5th week of scheduled order meals
        if len(delivery_dates) == 4:
            last_scheduled_order_meal_date = delivery_dates[-1]
            schedule_meals = schedule_meal_service.get_schedule_meals(
                meal_subscription_id=meal_subscription_id
            )
            for schedule_meal in schedule_meals:
                new_scheduled_order_meal_id = uuid4()
                new_scheduled_order_meal = Scheduled_Order_Meal_Domain(
                    scheduled_order_meal_object=None,
                    schedule_meal_object=schedule_meal,
                    scheduled_order_meal_id=new_scheduled_order_meal_id,
                    delivery_date=date_service.get_next_week_delivery_date(
                        last_scheduled_order_meal_date
                    ),
                    is_paused=is_paused,
                )
                self.scheduled_order_meal_repository.create_scheduled_order_meal(
                    scheduled_order_meal=new_scheduled_order_meal
                )

        return

    def check_if_first_week_of_meals(self, meal_subscription_id: UUID) -> bool:
        delivery_dates = self.get_current_scheduled_order_meal_delivery_dates(
            meal_subscription_id=meal_subscription_id
        )
        today = datetime.now(timezone.utc)
        print("delivery_dates", delivery_dates)
        if delivery_dates[0] >= today.timestamp():
            return True
        else:
            return False
