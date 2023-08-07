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
