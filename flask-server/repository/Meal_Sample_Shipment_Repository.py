from repository.Base_Repository import Base_Repository
from models import Meal_Sample_Shipment_Model
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from domain.Meal_Sample_Shipment_Domain import Meal_Sample_Shipment_Domain


class Meal_Sample_Shipment_Repository(Base_Repository):
    def create_shipment(
        self, meal_sample_shipment: "Meal_Sample_Shipment_Domain"
    ) -> None:
        new_meal_sample_shipment = Meal_Sample_Shipment_Model(
            meal_sample_shipment_domain=meal_sample_shipment
        )
        self.db.session.add(new_meal_sample_shipment)
        self.db.session.commit()
        return

    def get_meal_sample_shipment(
        self, dietitian_id: str
    ) -> Optional[Meal_Sample_Shipment_Model]:
        meal_sample_shipment = (
            self.db.session.query(Meal_Sample_Shipment_Model)
            .filter(Meal_Sample_Shipment_Model.dietitian_id == dietitian_id)
            .first()
        )
        return meal_sample_shipment
