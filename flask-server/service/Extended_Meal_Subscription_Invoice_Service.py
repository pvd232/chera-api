from .Meal_Subscription_Invoice_Service import Meal_Subscription_Invoice_Service
from domain.Extended_Meal_Subscription_Invoice_Domain import Extended_Meal_Subscription_Invoice_Domain
from datetime import datetime


class Extended_Meal_Subscription_Invoice_Service(Meal_Subscription_Invoice_Service):
    def get_upcoming_extended_meal_subscription_invoices(self, delivery_date: datetime) -> list['Extended_Meal_Subscription_Invoice_Domain']:
        upcoming_meal_subscription_invoices = self.meal_subscription_invoice_repository.get_upcoming_meal_subscription_invoices(
            delivery_date=delivery_date)
        return [Extended_Meal_Subscription_Invoice_Domain(meal_subscription_invoice_model=x) for x in upcoming_meal_subscription_invoices]
