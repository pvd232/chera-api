from domain.Scheduled_Order_Snack_Domain import Scheduled_Order_Snack_Domain
from datetime import datetime, timezone
from uuid import UUID, uuid4
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from models import Scheduled_Order_Snack_Model
    from repository.Scheduled_Order_Snack_Repository import (
        Scheduled_Order_Snack_Repository,
    )
    from service.Schedule_Snack_Service import Schedule_Snack_Service
    from service.Date_Service import Date_Service
    from dto.Scheduled_Order_Snack_DTO import Scheduled_Order_Snack_DTO


class Scheduled_Order_Snack_Service(object):
    def __init__(
        self, scheduled_order_snack_repository: "Scheduled_Order_Snack_Repository"
    ) -> None:
        self.scheduled_order_snack_repository = scheduled_order_snack_repository

    def update_scheduled_order_snacks(
        self, scheduled_order_snack_dtos: list["Scheduled_Order_Snack_DTO"]
    ) -> None:
        scheduled_order_snack_domains = [
            Scheduled_Order_Snack_Domain(
                scheduled_order_snack_object=x,
                schedule_snack_object=None,
                scheduled_order_snack_id=None,
                delivery_date=None,
                is_paused=None,
            )
            for x in scheduled_order_snack_dtos
        ]
        self.scheduled_order_snack_repository.update_scheduled_order_snacks(
            scheduled_order_snacks=scheduled_order_snack_domains
        )
        return

    def skip_weekly_scheduled_order_snacks(
        self, meal_subscription_id: UUID, delivery_date: float
    ) -> None:
        self.scheduled_order_snack_repository.skip_weekly_scheduled_order_snacks(
            meal_subscription_id=meal_subscription_id, delivery_date=delivery_date
        )
        return

    def unskip_weekly_scheduled_order_snacks(
        self, meal_subscription_id: UUID, delivery_date: float
    ) -> None:
        self.scheduled_order_snack_repository.unskip_weekly_scheduled_order_snacks(
            meal_subscription_id=meal_subscription_id, delivery_date=delivery_date
        )
        return

    def update_home_page_scheduled_order_snacks(
        self, scheduled_order_snack_dtos: list["Scheduled_Order_Snack_DTO"]
    ) -> None:
        scheduled_order_snack_domains = [
            Scheduled_Order_Snack_Domain(
                scheduled_order_snack_object=x,
                schedule_snack_object=None,
                scheduled_order_snack_id=None,
                delivery_date=None,
                is_paused=None,
            )
            for x in scheduled_order_snack_dtos
        ]
        self.scheduled_order_snack_repository.update_home_page_scheduled_order_snacks(
            meal_subscription_id=scheduled_order_snack_domains[0].meal_subscription_id,
            updated_scheduled_order_snacks=scheduled_order_snack_domains,
        )
        return

    def unpause_scheduled_order_snacks(self, meal_subscription_id: UUID) -> None:
        self.scheduled_order_snack_repository.unpause_scheduled_order_snacks(
            meal_subscription_id=meal_subscription_id
        )
        return

    def pause_scheduled_order_snacks(self, meal_subscription_id: UUID) -> None:
        self.scheduled_order_snack_repository.pause_scheduled_order_snacks(
            meal_subscription_id=meal_subscription_id
        )
        return

    # Delete all scheduled order meals for a meal subscription when client changes weekly meals
    def delete_scheduled_order_snacks(
        self,
        meal_subscription_id: UUID,
        cutoff_date: float,
        current_week_delivery_date: float,
        is_first_week: bool,
    ) -> None:
        self.scheduled_order_snack_repository.delete_scheduled_order_snacks(
            meal_subscription_id=meal_subscription_id,
            cutoff_date=cutoff_date,
            current_week_delivery_date=current_week_delivery_date,
            is_first_week=is_first_week,
        )
        return

    def create_scheduled_order_snack(
        self, scheduled_order_snack: Scheduled_Order_Snack_Domain
    ) -> None:
        self.scheduled_order_snack_repository.create_scheduled_order_snacks(
            scheduled_order_snack_domain=scheduled_order_snack
        )

    def create_scheduled_order_snacks(
        self, scheduled_order_snack_dtos: list["Scheduled_Order_Snack_DTO"]
    ) -> None:
        scheduled_order_snack_domains = [
            Scheduled_Order_Snack_Domain(
                scheduled_order_snack_object=x,
                schedule_snack_object=None,
                scheduled_order_snack_id=None,
                delivery_date=None,
                is_paused=None,
            )
            for x in scheduled_order_snack_dtos
        ]
        self.scheduled_order_snack_repository.create_scheduled_order_snacks(
            scheduled_order_snack_domains=scheduled_order_snack_domains
        )
        return

    def get_upcoming_scheduled_order_snacks(
        self, meal_subscription_id: UUID
    ) -> Optional[list[Scheduled_Order_Snack_Domain]]:
        scheduled_order_snacks: Optional[
            list["Scheduled_Order_Snack_Model"]
        ] = self.scheduled_order_snack_repository.get_scheduled_order_snacks(
            meal_subscription_id=meal_subscription_id
        )
        if scheduled_order_snacks:
            return [
                Scheduled_Order_Snack_Domain(
                    scheduled_order_snack_object=x,
                    schedule_snack_object=None,
                    scheduled_order_snack_id=None,
                    delivery_date=None,
                    is_paused=None,
                )
                for x in scheduled_order_snacks
            ]
        else:
            return None

    def get_scheduled_order_snacks(
        self, meal_subscription_id: Optional[UUID]
    ) -> Optional[list[Scheduled_Order_Snack_Domain]]:
        scheduled_order_snacks: Optional[
            list["Scheduled_Order_Snack_Model"]
        ] = self.scheduled_order_snack_repository.get_scheduled_order_snacks(
            meal_subscription_id=meal_subscription_id
        )
        if scheduled_order_snacks:
            return [
                Scheduled_Order_Snack_Domain(
                    scheduled_order_snack_object=x,
                    schedule_snack_object=None,
                    scheduled_order_snack_id=None,
                    delivery_date=None,
                    is_paused=None,
                )
                for x in scheduled_order_snacks
            ]
        else:
            return None

    def get_scheduled_order_snacks_for_week(
        self, meal_subscription_id: UUID, delivery_date: float
    ) -> Optional[list[Scheduled_Order_Snack_Domain]]:
        weekly_scheduled_order_snack_models = (
            self.scheduled_order_snack_repository.get_scheduled_order_snacks_for_week(
                meal_subscription_id=meal_subscription_id, delivery_date=delivery_date
            )
        )
        if weekly_scheduled_order_snack_models:
            weekly_scheduled_order_snack_domains: list[Scheduled_Order_Snack_Domain] = [
                Scheduled_Order_Snack_Domain(
                    scheduled_order_snack_object=x,
                    schedule_snack_object=None,
                    scheduled_order_snack_id=None,
                    delivery_date=None,
                    is_paused=None,
                )
                for x in weekly_scheduled_order_snack_models
            ]
            return weekly_scheduled_order_snack_domains
        else:
            return None

    def get_current_scheduled_order_snack_delivery_dates(
        self, meal_subscription_id: UUID
    ) -> Optional[list[float]]:
        scheduled_order_snacks: Optional[
            list[Scheduled_Order_Snack_Domain]
        ] = self.get_scheduled_order_snacks(meal_subscription_id=meal_subscription_id)
        if scheduled_order_snacks:
            date_dict = {}
            for snack in scheduled_order_snacks:
                # Check if delivery date is in the future and not already in the dictionary
                if (
                    snack.delivery_date > datetime.now(timezone.utc).timestamp()
                    and snack.delivery_date not in date_dict
                ):
                    date_dict[snack.delivery_date] = ""
            date_list = list(date_dict.keys())
            date_list.sort()
            return date_list
        else:
            return None

    # Create new scheduled order meals on weekly basis when stripe generates invoice
    def refresh_scheduled_order_snacks(
        self,
        meal_subscription_id: UUID,
        schedule_snack_service: "Schedule_Snack_Service",
        date_service: "Date_Service",
        is_paused: bool,
    ) -> None:
        delivery_dates = date_service.get_upcoming_delivery_dates()
        # If there are only 4 upcoming delivery dates then add the 5th week of scheduled order snacks
        if len(delivery_dates) == 4:
            last_scheduled_order_snack_date = delivery_dates[-1]
            schedule_snacks = schedule_snack_service.get_schedule_snacks(
                meal_subscription_id=meal_subscription_id
            )
            for schedule_snack in schedule_snacks:
                new_scheduled_order_snack_id = uuid4()
                new_scheduled_order_snack = Scheduled_Order_Snack_Domain(
                    scheduled_order_snack_object=None,
                    schedule_snack_object=schedule_snack,
                    scheduled_order_snack_id=new_scheduled_order_snack_id,
                    delivery_date=date_service.get_next_week_delivery_date(
                        last_scheduled_order_snack_date
                    ),
                    is_paused=is_paused,
                )
                self.scheduled_order_snack_repository.create_scheduled_order_snack(
                    scheduled_order_snack=new_scheduled_order_snack
                )

        return

    def check_if_first_week_of_snacks(self, meal_subscription_id: UUID) -> bool:
        delivery_dates = self.get_current_scheduled_order_snack_delivery_dates(
            meal_subscription_id=meal_subscription_id
        )
        today = datetime.now(timezone.utc)
        if delivery_dates[0] >= today.timestamp():
            return True
        else:
            return False
