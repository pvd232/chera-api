from repository.Base_Repository import Base_Repository
from models import Meal_Sample_Model, Meal_Subscription_Invoice_Model
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from domain.Meal_Sample_Domain import Meal_Sample_Domain


class Meal_Sample_Repository(Base_Repository):
    def create_meal_samples(
        self, meal_sample_domains: list["Meal_Sample_Domain"]
    ) -> None:
        for meal_sample_domain in meal_sample_domains:
            new_meal_sample = Meal_Sample_Model(meal_sample_domain=meal_sample_domain)
            self.db.session.add(new_meal_sample)
        self.db.session.commit()
        return

    def get_meal_samples(self, dietitian_id: str) -> Optional[list[Meal_Sample_Model]]:
        meal_samples_to_return: list[Meal_Sample_Model] = []
        meal_subscription_invoices: Optional[
            list[Meal_Subscription_Invoice_Model]
        ] = self.db.session.query(Meal_Subscription_Invoice_Model).filter(
            Meal_Subscription_Invoice_Model.dietitian_id == dietitian_id
        )
        if meal_subscription_invoices:
            for meal_subscription_invoice in meal_subscription_invoices:
                for meal_sample in meal_subscription_invoice.meal_samples:
                    meal_samples_to_return.append(meal_sample)
            return meal_samples_to_return
        else:
            return None
