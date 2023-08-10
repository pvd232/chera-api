from repository.Base_Repository import Base_Repository
from models import Meal_Sample_Model
from typing import TYPE_CHECKING

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

    def get_meal_samples(self):
        meal_sample_objects = self.db.session.query(Meal_Sample_Model).all()
        return meal_sample_objects

    def initialize_meal_samples(self, dietitian_dict) -> None:
        from pathlib import Path
        from utils.load_json import load_json
        from domain.Meal_Sample_Domain import Meal_Sample_Domain
        from dto.Meal_Sample_DTO import Meal_Sample_DTO

        meal_sample_json_file = Path(".", "dietitian_data", "meal_samples.json")
        meal_samples_data = load_json(filename=meal_sample_json_file)

        for meal_sample_json in meal_samples_data:
            # Pass in dietitian dict with email as key and updated dietitian object as value
            matching_dietitian = dietitian_dict[meal_sample_json["dietitian_id"]]
            meal_sample_json["dietitian_id"] = matching_dietitian["id"]
            meal_sample_dto = Meal_Sample_DTO(meal_sample_json=meal_sample_json)
            meal_sample_domain = Meal_Sample_Domain(meal_sample_object=meal_sample_dto)
            meal_sample_model = Meal_Sample_Model(meal_sample_domain=meal_sample_domain)
            self.db.session.add(meal_sample_model)
        self.db.session.commit()
