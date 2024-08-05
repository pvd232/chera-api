from uuid import UUID
from typing import TYPE_CHECKING, Optional
from .Base_DTO import Base_DTO

if TYPE_CHECKING:
    from domain.Meal_Plan_Domain import Meal_Plan_Domain


class Meal_Plan_DTO(Base_DTO):
    def __init__(
        self,
        meal_plan_json: Optional[dict] = None,
        meal_plan_domain: "Meal_Plan_Domain" = None,
    ) -> None:
        if meal_plan_json:
            self.id: UUID = UUID(meal_plan_json["id"])
            self.number: int = int(meal_plan_json["number"])
            self.breakfast_calories = int(meal_plan_json["breakfast_calories"])
            self.lunch_calories = int(meal_plan_json["lunch_calories"])
            self.dinner_calories = int(meal_plan_json["dinner_calories"])
            self.stated_caloric_lower_bound = int(
                meal_plan_json["stated_caloric_lower_bound"]
            )
            self.stated_caloric_upper_bound = int(
                meal_plan_json["stated_caloric_upper_bound"]
            )
            self.number_of_snacks = int(meal_plan_json["number_of_snacks"])
            self.per_snack_caloric_lower_bound = int(
                meal_plan_json["per_snack_caloric_lower_bound"]
            )
            self.per_snack_caloric_upper_bound = int(
                meal_plan_json["per_snack_caloric_upper_bound"]
            )
        elif meal_plan_domain:
            self.id: UUID = meal_plan_domain.id
            self.number: int = meal_plan_domain.number
            self.breakfast_calories: int = meal_plan_domain.breakfast_calories
            self.lunch_calories: int = meal_plan_domain.lunch_calories
            self.dinner_calories: int = meal_plan_domain.dinner_calories
            self.stated_caloric_lower_bound: int = (
                meal_plan_domain.stated_caloric_lower_bound
            )
            self.stated_caloric_upper_bound: int = (
                meal_plan_domain.stated_caloric_upper_bound
            )
            self.number_of_snacks: int = meal_plan_domain.number_of_snacks
            self.per_snack_caloric_lower_bound: int = (
                meal_plan_domain.per_snack_caloric_lower_bound
            )
            self.per_snack_caloric_upper_bound: int = (
                meal_plan_domain.per_snack_caloric_upper_bound
            )
