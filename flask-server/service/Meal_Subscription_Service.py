from domain.Meal_Subscription_Domain import Meal_Subscription_Domain
from uuid import UUID
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from models import Meal_Subscription_Model
    from repository.Meal_Subscription_Repository import Meal_Subscription_Repository
    from service.Stripe_Service import Stripe_Service
    from service.Scheduled_Order_Meal_Service import Scheduled_Order_Meal_Service
    from service.Schedule_Meal_Service import Schedule_Meal_Service
    from service.Date_Service import Date_Service
    from dto.Meal_Subscription_DTO import Meal_Subscription_DTO


class Meal_Subscription_Service(object):
    def __init__(
        self, meal_subscription_repository: "Meal_Subscription_Repository"
    ) -> None:
        self.meal_subscription_repository = meal_subscription_repository

    def get_meal_subscriptions(self) -> list[Meal_Subscription_Domain]:
        meal_subscription_domains: list[Meal_Subscription_Domain] = [
            Meal_Subscription_Domain(meal_subscription_object=x)
            for x in self.meal_subscription_repository.get_meal_subscriptions()
        ]
        return meal_subscription_domains

    def get_meal_subscription(
        self,
        meal_subscription_id: UUID = None,
        stripe_subscription_id: str = None,
        client_id: str = None,
    ) -> Optional[Meal_Subscription_Domain]:
        if meal_subscription_id:
            meal_subscription_object = (
                self.meal_subscription_repository.get_meal_subscription(
                    meal_subscription_id=meal_subscription_id
                )
            )
            if meal_subscription_object:
                meal_subscription_domain = Meal_Subscription_Domain(
                    meal_subscription_object=meal_subscription_object
                )
                return meal_subscription_domain
        elif stripe_subscription_id:
            meal_subscription_object = (
                self.meal_subscription_repository.get_meal_subscription(
                    stripe_subscription_id=stripe_subscription_id
                )
            )
            if meal_subscription_object:
                meal_subscription_domain = Meal_Subscription_Domain(
                    meal_subscription_object=meal_subscription_object
                )
                return meal_subscription_domain
        elif client_id:
            meal_subscription_object = (
                self.meal_subscription_repository.get_meal_subscription(
                    client_id=client_id
                )
            )
            if meal_subscription_object:
                meal_subscription_domain = Meal_Subscription_Domain(
                    meal_subscription_object=meal_subscription_object
                )
                return meal_subscription_domain
        return None

    def get_active_meal_subscriptions(self) -> list[Meal_Subscription_Domain]:
        active_meal_subscription_models = (
            self.meal_subscription_repository.get_active_meal_subscriptions()
        )
        active_meal_subscription_domains = [
            Meal_Subscription_Domain(meal_subscription_object=x)
            for x in active_meal_subscription_models
        ]
        return active_meal_subscription_domains

    def create_meal_subscription(
        self, meal_subscription_dto: "Meal_Subscription_DTO", shipping_cost: float
    ) -> Meal_Subscription_Domain:
        # Create meal subscription
        requested_meal_subscription = Meal_Subscription_Domain(
            meal_subscription_object=meal_subscription_dto
        )

        requested_meal_subscription.shipping_cost = shipping_cost
        self.meal_subscription_repository.create_meal_subscription(
            meal_subscription_domain=requested_meal_subscription
        )
        return requested_meal_subscription

    def pause_meal_subscription(
        self, meal_subscription_id: UUID, stripe_service: "Stripe_Service"
    ) -> None:
        # Get the meal subscription
        meal_subscription_to_pause: Optional[
            Meal_Subscription_Domain
        ] = self.get_meal_subscription(meal_subscription_id=meal_subscription_id)
        if meal_subscription_to_pause:
            # Pause the meal subscription
            self.meal_subscription_repository.pause_meal_subscription(
                meal_subscription_id=meal_subscription_id
            )
            # Pause the stripe subscription
            stripe_service.pause_stripe_subscription(
                stripe_subscription_id=meal_subscription_to_pause.stripe_subscription_id
            )
        return

    def unpause_meal_subscription(
        self, meal_subscription_id: UUID, stripe_service: "Stripe_Service"
    ) -> None:
        meal_subscription_to_unpause = self.get_meal_subscription(
            meal_subscription_id=meal_subscription_id
        )
        if meal_subscription_to_unpause:
            self.meal_subscription_repository.unpause_meal_subscription(
                meal_subscription_id=meal_subscription_to_unpause.id
            )
            stripe_service.unpause_stripe_subscription(
                stripe_subscription_id=meal_subscription_to_unpause.stripe_subscription_id
            )
        return

    def get_client_meal_subscription(
        self, client_id: str
    ) -> Optional[Meal_Subscription_Domain]:
        client_meal_subscription: Optional[
            "Meal_Subscription_Model"
        ] = self.meal_subscription_repository.get_client_meal_subscription(
            client_id=client_id
        )
        if client_meal_subscription:
            return Meal_Subscription_Domain(
                meal_subscription_object=client_meal_subscription
            )
        else:
            None

    def get_dietitian_meal_subscriptions(
        self, dietitian_id: str = None
    ) -> Optional[list[Meal_Subscription_Domain]]:
        meal_subscription_models = (
            self.meal_subscription_repository.get_dietitian_meal_subscriptions(
                dietitian_id=dietitian_id
            )
        )
        if meal_subscription_models:
            return [
                Meal_Subscription_Domain(meal_subscription_object=x)
                for x in meal_subscription_models
            ]
        else:
            return None

    def refresh_meal_subscriptions(
        self,
        scheduled_order_meal_service: "Scheduled_Order_Meal_Service",
        schedule_meal_service: "Schedule_Meal_Service",
        date_service: "Date_Service",
    ) -> None:
        meals_subscriptions = self.get_meal_subscriptions()
        for meal_subscrpition in meals_subscriptions:
            scheduled_order_meal_service.refresh_scheduled_order_meals(
                meal_subscription_id=meal_subscrpition.id,
                schedule_meal_service=schedule_meal_service,
                date_service=date_service,
                is_paused=meal_subscrpition.paused,
            )
        return
