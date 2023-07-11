from models import Meal_Subscription_Model
from .Base_Domain import Base_Domain
from dto.Meal_Subscription_DTO import Meal_Subscription_DTO
from datetime import datetime


class Meal_Subscription_Domain(Base_Domain):
    def __init__(
        self, meal_subscription_object: Meal_Subscription_Model | Meal_Subscription_DTO
    ) -> None:
        self.id = meal_subscription_object.id
        self.client_id = meal_subscription_object.client_id
        self.dietitian_id = meal_subscription_object.dietitian_id
        self.stripe_subscription_id = meal_subscription_object.stripe_subscription_id
        self.shipping_rate = meal_subscription_object.shipping_rate
        self.datetime = meal_subscription_object.datetime
        self.paused = meal_subscription_object.paused
        self.active = meal_subscription_object.active
