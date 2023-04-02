from repository.Base_Repository import Base_Repository
from models import Meal_Shipment_Model
from uuid import UUID
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from domain.Meal_Shipment_Domain import Meal_Shipment_Domain


class Meal_Shipment_Repository(Base_Repository):
    def create_shipment(self,  meal_shipment: 'Meal_Shipment_Domain') -> None:
        new_meal_shipment: Meal_Shipment_Model = Meal_Shipment_Model(
            meal_shipment=meal_shipment)
        self.db.session.add(new_meal_shipment)
        self.db.session.commit()
        return

    def get_meal_shipment(self,  meal_subscription_invoice_id: UUID) -> Optional[Meal_Shipment_Model]:
        meal_shipment = self.db.session.query(Meal_Shipment_Model).filter(
            Meal_Shipment_Model.meal_subscription_invoice_id == meal_subscription_invoice_id).first()
        return meal_shipment
