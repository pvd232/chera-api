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

    def get_meal_sample_shipments(self):
        meal_sample_shipment_objects = self.db.session.query(
            Meal_Sample_Shipment_Model
        ).all()
        return meal_sample_shipment_objects

    def initialize_meal_sample_shipments(self) -> None:
        from pathlib import Path
        from utils.load_json import load_json
        from domain.Meal_Sample_Shipment_Domain import Meal_Sample_Shipment_Domain

        meal_sample_json_file = Path(
            ".", "dietitian_data", "meal_sample_shipments.json"
        )
        meal_sample_shipment_data = load_json(filename=meal_sample_json_file)

        for meal_sample_shipment_json in meal_sample_shipment_data:
            meal_sample_shipment_domain = Meal_Sample_Shipment_Domain(
                meal_sample_shipment_json=meal_sample_shipment_json
            )
            meal_sample_shipment_model = Meal_Sample_Shipment_Model(
                meal_sample_shipment_domain=meal_sample_shipment_domain
            )
            self.db.session.add(meal_sample_shipment_model)
        self.db.session.commit()
