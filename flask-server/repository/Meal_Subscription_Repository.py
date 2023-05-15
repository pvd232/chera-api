from repository.Base_Repository import Base_Repository
from models import Meal_Subscription_Model
from uuid import UUID
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from domain.Meal_Subscription_Domain import Meal_Subscription_Domain


class Meal_Subscription_Repository(Base_Repository):
    def get_meal_subscriptions(self) -> Optional[list[Meal_Subscription_Model]]:
        meal_subscriptions = self.db.session.query(Meal_Subscription_Model).all()
        return meal_subscriptions

    def get_meal_subscription(
        self,
        meal_subscription_id: UUID = None,
        stripe_subscription_id: str = None,
    ) -> Optional[Meal_Subscription_Model]:
        if meal_subscription_id:
            subscription = (
                self.db.session.query(Meal_Subscription_Model)
                .filter(Meal_Subscription_Model.id == meal_subscription_id)
                .first()
            )
        elif stripe_subscription_id:
            subscription = (
                self.db.session.query(Meal_Subscription_Model)
                .filter(
                    Meal_Subscription_Model.stripe_subscription_id
                    == stripe_subscription_id
                )
                .first()
            )
        return subscription

    def get_active_meal_subscriptions(self) -> Optional[list[Meal_Subscription_Model]]:
        meal_subscriptions = self.db.session.query(Meal_Subscription_Model).filter(
            Meal_Subscription_Model.paused == False,
            Meal_Subscription_Model.active == True,
        )
        return meal_subscriptions

    def create_meal_subscription(
        self, meal_subscription_domain: "Meal_Subscription_Domain"
    ) -> None:
        new_subscription: Meal_Subscription_Model = Meal_Subscription_Model(
            meal_subscription=meal_subscription_domain
        )
        self.db.session.add(new_subscription)
        self.db.session.commit()
        return

    def update_meal_subscription(
        self, meal_subscription_domain: "Meal_Subscription_Domain"
    ) -> UUID:
        update_subscription: Meal_Subscription_Model = (
            self.get_client_meal_subscription(
                client_id=meal_subscription_domain.client_id
            )
        )
        update_subscription.update(meal_subscription_domain=meal_subscription_domain)
        self.db.session.commit()
        # The id is the only property predicated on the previous subscription that needs to be refreshed and returned to the service layer
        return update_subscription.id

    def pause_meal_subscription(self, meal_subscription_id: UUID) -> None:
        meal_subscription_to_pause: Meal_Subscription_Model = (
            self.db.session.query(Meal_Subscription_Model)
            .filter(Meal_Subscription_Model.id == meal_subscription_id)
            .first()
        )
        meal_subscription_to_pause.paused = True
        self.db.session.commit()

    def unpause_meal_subscription(self, meal_subscription_id: UUID) -> None:
        meal_subscription_to_unpause: Meal_Subscription_Model = (
            self.db.session.query(Meal_Subscription_Model)
            .filter(Meal_Subscription_Model.id == meal_subscription_id)
            .first()
        )
        if meal_subscription_to_unpause:
            meal_subscription_to_unpause.paused = False
            self.db.session.commit()
        return

    def deactivate_meal_subscription(self, meal_subscription_id: UUID) -> None:
        meal_subscription_to_deactivate: Meal_Subscription_Model = (
            self.get_meal_subscription(meal_subscription_id=meal_subscription_id)
        )
        if meal_subscription_to_deactivate:
            meal_subscription_to_deactivate.active = False
            self.db.session.commit()
        return

    def get_client_meal_subscription(
        self, client_id: str = None
    ) -> Optional[Meal_Subscription_Model]:
        meal_subscription: Optional[Meal_Subscription_Model] = (
            self.db.session.query(Meal_Subscription_Model)
            .filter(
                Meal_Subscription_Model.client_id == client_id,
                Meal_Subscription_Model.active == True,
            )
            .first()
        )
        if meal_subscription != None:
            return meal_subscription
        else:
            return False

    def get_dietitian_meal_subscriptions(
        self, dietitian_id: str = None
    ) -> Optional[list[Meal_Subscription_Model]]:
        if dietitian_id:
            meal_subscriptions = self.db.session.query(Meal_Subscription_Model).filter(
                Meal_Subscription_Model.dietitian_id == dietitian_id,
                Meal_Subscription_Model.active == True,
            )
        else:
            meal_subscriptions = self.db.session.query(Meal_Subscription_Model).all()
        return meal_subscriptions
