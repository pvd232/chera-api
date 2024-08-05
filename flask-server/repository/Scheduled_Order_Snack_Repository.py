from repository.Base_Repository import Base_Repository
from models import Scheduled_Order_Snack_Model
from uuid import UUID
from datetime import datetime, timedelta, timezone
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from domain.Scheduled_Order_Snack_Domain import Scheduled_Order_Snack_Domain


class Scheduled_Order_Snack_Repository(Base_Repository):
    def get_upcoming_scheduled_order_snacks(
        self, meal_subscription_id: UUID
    ) -> Optional[list[Scheduled_Order_Snack_Model]]:
        scheduled_order_snacks = (
            self.db.session.query(Scheduled_Order_Snack_Model)
            .filter(
                Scheduled_Order_Snack_Model.meal_subscription_id
                == meal_subscription_id,
                Scheduled_Order_Snack_Model.delivery_date
                > datetime.now(timezone.utc).timestamp(),
            )
            .all()
        )
        if scheduled_order_snacks:
            return scheduled_order_snacks
        else:
            return None

    def get_scheduled_order_snacks(
        self, meal_subscription_id: Optional[UUID] = None
    ) -> Optional[list[Scheduled_Order_Snack_Model]]:
        if meal_subscription_id:
            scheduled_order_snacks: Optional[
                list[Scheduled_Order_Snack_Model]
            ] = self.db.session.query(Scheduled_Order_Snack_Model).filter(
                Scheduled_Order_Snack_Model.meal_subscription_id == meal_subscription_id
            )
            if scheduled_order_snacks:
                return scheduled_order_snacks
            else:
                return False
        else:
            scheduled_order_snacks: Optional[list[Scheduled_Order_Snack_Model]] = (
                self.db.session.query(Scheduled_Order_Snack_Model).all()
            )
        return scheduled_order_snacks

    def get_scheduled_order_snacks_for_week(
        self, meal_subscription_id: UUID, delivery_date: float
    ) -> Optional[list[Scheduled_Order_Snack_Model]]:
        weekly_scheduled_order_snacks = (
            self.db.session.query(Scheduled_Order_Snack_Model)
            .filter(
                Scheduled_Order_Snack_Model.meal_subscription_id
                == meal_subscription_id,
                Scheduled_Order_Snack_Model.delivery_date == delivery_date,
            )
            .all()
        )
        return weekly_scheduled_order_snacks

    def create_scheduled_order_snacks(
        self, scheduled_order_snack_domains: list["Scheduled_Order_Snack_Domain"]
    ) -> None:
        for scheduled_order_snack_domain in scheduled_order_snack_domains:
            new_scheduled_order_snack = Scheduled_Order_Snack_Model(
                scheduled_order_snack_domain=scheduled_order_snack_domain
            )
            self.db.session.add(new_scheduled_order_snack)
        self.db.session.commit()

        return

    def update_home_page_scheduled_order_snacks(
        self,
        meal_subscription_id: UUID,
        updated_scheduled_order_snacks: list["Scheduled_Order_Snack_Domain"],
    ) -> None:
        current_scheduled_order_snacks = self.get_upcoming_scheduled_order_snacks(
            meal_subscription_id=meal_subscription_id
        )
        current_scheduled_order_snacks_map = {}

        # Create a map of the current scheduled order meals
        for current_scheduled_order_snack in current_scheduled_order_snacks:
            current_scheduled_order_snacks_map[
                str(current_scheduled_order_snack.id)
            ] = ""

        for updated_scheduled_order_snack in updated_scheduled_order_snacks:
            # If the updated scheduled order meal is not in the current scheduled order meals map, then it is a new scheduled order meal
            if (
                str(updated_scheduled_order_snack.id)
                not in current_scheduled_order_snacks_map
            ):
                new_scheduled_order_snack = Scheduled_Order_Snack_Model(
                    scheduled_order_snack_domain=updated_scheduled_order_snack
                )
                self.db.session.add(new_scheduled_order_snack)
            # Otherwise, it is an unchanged existing scheduled order meal and is removed from the current scheduled order meals map
            else:
                current_scheduled_order_snacks_map.pop(
                    str(updated_scheduled_order_snack.id)
                )

        # All remaining scheduled order meals in the current scheduled order meals map are scheduled order meals that have been removed
        for scheduled_order_snack_id in current_scheduled_order_snacks_map.keys():
            scheduled_order_snack_to_delete = (
                self.db.session.query(Scheduled_Order_Snack_Model)
                .filter(
                    Scheduled_Order_Snack_Model.id == UUID(scheduled_order_snack_id)
                )
                .first()
            )
            self.db.session.delete(scheduled_order_snack_to_delete)
        self.db.session.commit()
        return

    def skip_weekly_scheduled_order_snacks(
        self, meal_subscription_id: UUID, delivery_date: float
    ) -> None:
        weekly_scheduled_order_snacks = (
            self.db.session.query(Scheduled_Order_Snack_Model)
            .filter(
                Scheduled_Order_Snack_Model.meal_subscription_id
                == meal_subscription_id,
                Scheduled_Order_Snack_Model.delivery_date == delivery_date,
            )
            .all()
        )
        for scheduled_order_snack in weekly_scheduled_order_snacks:
            scheduled_order_snack.delivery_skipped = True
        self.db.session.commit()
        return

    def unskip_weekly_scheduled_order_snacks(
        self, meal_subscription_id: UUID, delivery_date: float
    ) -> None:
        weekly_scheduled_order_snacks = (
            self.db.session.query(Scheduled_Order_Snack_Model)
            .filter(
                Scheduled_Order_Snack_Model.meal_subscription_id
                == meal_subscription_id,
                Scheduled_Order_Snack_Model.delivery_date == delivery_date,
            )
            .all()
        )
        for scheduled_order_snack in weekly_scheduled_order_snacks:
            scheduled_order_snack.delivery_skipped = False
        self.db.session.commit()
        return

    def update_scheduled_order_snacks(
        self, scheduled_order_snacks: list["Scheduled_Order_Snack_Domain"]
    ) -> None:
        for scheduled_order_snack in scheduled_order_snacks:
            scheduled_order_snack_to_update: Scheduled_Order_Snack_Model = (
                self.db.session.query(Scheduled_Order_Snack_Model)
                .filter(Scheduled_Order_Snack_Model.id == scheduled_order_snack.id)
                .first()
            )
            scheduled_order_snack_to_update.delivery_skipped = (
                scheduled_order_snack.delivery_skipped
            )
        self.db.session.commit()

        return

    def pause_scheduled_order_snacks(self, meal_subscription_id: UUID) -> None:
        scheduled_order_snacks_to_pause = self.get_upcoming_scheduled_order_snacks(
            meal_subscription_id=meal_subscription_id
        )
        for scheduled_order_snack in scheduled_order_snacks_to_pause:
            if self.can_pause_scheduled_order_snack(
                scheduled_order_snack=scheduled_order_snack
            ):
                scheduled_order_snack.paused = True
        self.db.session.commit()
        return

    def unpause_scheduled_order_snacks(self, meal_subscription_id: UUID) -> None:
        scheduled_order_snacks_to_unpause = self.get_upcoming_scheduled_order_snacks(
            meal_subscription_id=meal_subscription_id
        )
        for scheduled_order_snack in scheduled_order_snacks_to_unpause:
            scheduled_order_snack.paused = False
        self.db.session.commit()
        return

    def delete_scheduled_order_snacks(
        self,
        meal_subscription_id: UUID,
        cutoff_date: float,
        current_week_delivery_date: float,
        is_first_week: bool,
    ) -> None:
        scheduled_order_snacks_to_delete = self.get_upcoming_scheduled_order_snacks(
            meal_subscription_id=meal_subscription_id
        )
        today = datetime.now(timezone.utc).timestamp()
        for scheduled_order_snack in scheduled_order_snacks_to_delete:
            # Only delete the current week scheduled order meals if its before the cutoff date and it isnt the first week of the subscription
            if today < cutoff_date and not is_first_week:
                self.db.session.delete(scheduled_order_snack)
            else:
                if scheduled_order_snack.delivery_date > current_week_delivery_date:
                    self.db.session.delete(scheduled_order_snack)
            self.db.session.commit()
        return

    def can_pause_scheduled_order_snack(
        self, scheduled_order_snack: "Scheduled_Order_Snack_Domain"
    ) -> bool:
        if datetime.utcfromtimestamp(scheduled_order_snack.delivery_date).replace(
            tzinfo=timezone.utc
        ) - datetime.now(timezone.utc) > timedelta(days=2):
            return True
        else:
            return False
