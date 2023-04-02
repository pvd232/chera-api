from dto.USDA_Ingredient_DTO import USDA_Ingredient_DTO
from dto.USDA_Ingredient_Portion_DTO import USDA_Ingredient_Portion_DTO
from domain.Extended_USDA_Ingredient_Domain import Extended_USDA_Ingredient_Domain


class Extended_USDA_Ingredient_DTO(USDA_Ingredient_DTO):
    def __init__(self, extended_usda_ingredient_domain: 'Extended_USDA_Ingredient_Domain') -> None:
        super().__init__(usda_ingredient_domain=extended_usda_ingredient_domain)
        self.portions: list[USDA_Ingredient_Portion_DTO] = [USDA_Ingredient_Portion_DTO(
            usda_ingredient_portion_domain=x) for x in extended_usda_ingredient_domain.portions]

    def serialize(self) -> dict:
        attribute_names = list(self.__dict__.keys())
        attributes = list(self.__dict__.values())
        serialized_attributes = super().serialize()
        for i in range(len(attributes)):
            if attribute_names[i] == "portions":
                serialized_attributes[attribute_names[i]] = [
                    x.serialize() for x in attributes[i]]
        return serialized_attributes
