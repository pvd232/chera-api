from .Meal_Plan_DTO import Meal_Plan_DTO
from .USDA_Nutrient_Daily_Value_DTO import USDA_Nutrient_Daily_Value_DTO
from domain.Extended_Meal_Plan_Domain import Extended_Meal_Plan_Domain


class Extended_Meal_Plan_DTO(Meal_Plan_DTO):
    def __init__(self, extended_meal_plan_domain: 'Extended_Meal_Plan_Domain') -> None:
        super().__init__(meal_plan_domain=extended_meal_plan_domain)
        self.usda_nutrient_daily_values: list[USDA_Nutrient_Daily_Value_DTO] = [USDA_Nutrient_Daily_Value_DTO(
            usda_nutrient_daily_value_domain=x) for x in extended_meal_plan_domain.usda_nutrient_daily_values]

    def serialize(self) -> dict:
        attribute_names = list(self.__dict__.keys())
        attributes = list(self.__dict__.values())
        serialized_attributes = super().serialize()
        for i in range(len(attributes)):
            if attribute_names[i] == "usda_nutrient_daily_values":
                serialized_attributes[attribute_names[i]] = [
                    x.serialize() for x in attributes[i]]
        return serialized_attributes
