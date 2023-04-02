from .Base_Domain import Base_Domain
from models import Imperial_Ingredient_Unit_Model


class Imperial_Ingredient_Unit_Domain(Base_Domain):
    def __init__(self, imperial_ingredient_unit_object: Imperial_Ingredient_Unit_Model) -> None:
        self.id = imperial_ingredient_unit_object.id
        self.ounces = imperial_ingredient_unit_object.ounces
