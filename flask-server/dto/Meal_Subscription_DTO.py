from .Base_DTO import Base_DTO
from uuid import UUID
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from domain.Meal_Subscription_Domain import Meal_Subscription_Domain


class Meal_Subscription_DTO(Base_DTO):
    def __init__(
        self,
        meal_subscription_json: dict = None,
        meal_subscription_domain: "Meal_Subscription_Domain" = None,
    ) -> None:
        if meal_subscription_json:
            self.id: UUID = UUID(meal_subscription_json["id"])
            self.client_id: str = meal_subscription_json["client_id"]
            self.dietitian_id: Optional[UUID] = meal_subscription_json["dietitian_id"]
            self.stripe_subscription_id: str = meal_subscription_json[
                "stripe_subscription_id"
            ]
            self.shipping_rate: float = float(meal_subscription_json["shipping_rate"])
            self.datetime: float = float(meal_subscription_json["datetime"])
            self.paused: bool = meal_subscription_json["paused"]
            self.active: bool = meal_subscription_json["active"]
        elif meal_subscription_domain:
            self.id: UUID = meal_subscription_domain.id
            self.client_id: str = meal_subscription_domain.client_id
            self.dietitian_id: Optional[UUID] = meal_subscription_domain.dietitian_id
            self.stripe_subscription_id: str = (
                meal_subscription_domain.stripe_subscription_id
            )
            self.shipping_rate: float = meal_subscription_domain.shipping_rate
            self.datetime: float = meal_subscription_domain.datetime
            self.paused: bool = meal_subscription_domain.paused
            self.active: bool = meal_subscription_domain.active
