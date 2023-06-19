from repository.Base_Repository import Base_Repository
from models import USDA_Nutrient_Daily_Value_Model
from uuid import UUID


class USDA_Nutrient_Daily_Value_Repository(Base_Repository):
    def get_usda_nutrient_daily_values(self):
        usda_nutrient_daily_values = self.db.session.query(
            USDA_Nutrient_Daily_Value_Model
        ).all()
        return usda_nutrient_daily_values
    def get_usda_nutrient_daily_value(
        self, meal_plan_id: UUID, nutrient_id: str
    ) -> USDA_Nutrient_Daily_Value_Model:
        usda_nutrient_daily_value = (
            self.db.session.query(USDA_Nutrient_Daily_Value_Model)
            .filter(
                USDA_Nutrient_Daily_Value_Model.meal_plan_id == meal_plan_id,
                USDA_Nutrient_Daily_Value_Model.nutrient_id == nutrient_id,
            )
            .first()
        )
        return usda_nutrient_daily_value

    def initialize_usda_nutrient_daily_values(self) -> None:
        from pathlib import Path
        from utils.load_json import load_json
        from domain.USDA_Nutrient_Daily_Value_Domain import (
            USDA_Nutrient_Daily_Value_Domain,
        )
        from dto.USDA_Nutrient_Daily_Value_DTO import USDA_Nutrient_Daily_Value_DTO

        usda_nutrient_daily_value_json_file = Path(
            ".", "nutrient_data", "new_usda_nutrient_daily_values.json"
        )
        usda_nutrient_daily_values_data = load_json(
            filename=usda_nutrient_daily_value_json_file
        )

        # Only initialize custom values, not USDA values which are initialized alongside Usda_Nutrient_Daily_Value_Models
        for usda_nutrient_daily_value_json in usda_nutrient_daily_values_data:
            usda_nutrient_daily_value_dto = USDA_Nutrient_Daily_Value_DTO(
                usda_nutrient_daily_value_json=usda_nutrient_daily_value_json
            )
            usda_nutrient_daily_value_domain = USDA_Nutrient_Daily_Value_Domain(
                usda_nutrient_daily_value_object=usda_nutrient_daily_value_dto
            )

            new_usda_nutrient_daily_value_model = USDA_Nutrient_Daily_Value_Model(
                usda_nutrient_daily_value_domain=usda_nutrient_daily_value_domain
            )
            self.db.session.add(new_usda_nutrient_daily_value_model)
        self.db.session.commit()
