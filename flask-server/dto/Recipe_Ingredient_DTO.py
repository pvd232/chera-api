from uuid import UUID
from typing import TYPE_CHECKING
from .Base_DTO import Base_DTO
from typing import Optional

if TYPE_CHECKING:
    from domain.Recipe_Ingredient_Domain import Recipe_Ingredient_Domain


class Recipe_Ingredient_DTO(Base_DTO):
    def __init__(
        self,
        recipe_ingredient_json: dict = None,
        recipe_ingredient_domain: "Recipe_Ingredient_Domain" = None,
    ) -> None:
        if recipe_ingredient_json:
            self.id: UUID = UUID(recipe_ingredient_json["id"])
            self.usda_ingredient_id: UUID = recipe_ingredient_json["usda_ingredient_id"]
            self.meal_plan_meal_id: Optional[UUID] = recipe_ingredient_json[
                "meal_plan_meal_id"
            ]

            # Frontend sends empty string for null values, when reinstantiating the object, value will be None
            if self.meal_plan_meal_id == "" or self.meal_plan_meal_id == None:
                self.meal_plan_meal_id = ""
            else:
                self.meal_plan_meal_id = UUID(self.meal_plan_meal_id)

            self.meal_plan_snack_id: Optional[UUID] = recipe_ingredient_json[
                "meal_plan_snack_id"
            ]

            if self.meal_plan_snack_id == "" or self.meal_plan_snack_id == None:
                self.meal_plan_snack_id = ""
            else:
                self.meal_plan_snack_id = UUID(self.meal_plan_snack_id)

            self.usda_ingredient_portion_id: UUID = UUID(
                recipe_ingredient_json["usda_ingredient_portion_id"]
            )
            self.quantity: float = float(recipe_ingredient_json["quantity"])
            self.active: bool = recipe_ingredient_json["active"]

        elif recipe_ingredient_domain:
            self.id: UUID = recipe_ingredient_domain.id
            self.usda_ingredient_id: UUID = recipe_ingredient_domain.usda_ingredient_id
            self.meal_plan_meal_id: Optional[
                UUID
            ] = recipe_ingredient_domain.meal_plan_meal_id
            self.meal_plan_snack_id: Optional[
                UUID
            ] = recipe_ingredient_domain.meal_plan_snack_id
            self.usda_ingredient_portion_id: UUID = (
                recipe_ingredient_domain.usda_ingredient_portion_id
            )
            self.quantity: float = recipe_ingredient_domain.quantity
            self.active: bool = recipe_ingredient_domain.active
