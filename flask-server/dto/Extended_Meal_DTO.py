from dto.Meal_DTO import Meal_DTO
from dto.Meal_Dietary_Restriction_DTO import Meal_Dietary_Restriction_DTO
from domain.Extended_Meal_Domain import Extended_Meal_Domain


class Extended_Meal_DTO(Meal_DTO):
    def __init__(self, extended_meal_domain: 'Extended_Meal_Domain') -> None:
        super().__init__(meal_domain=extended_meal_domain)
        self.dietary_restrictions: list[Meal_Dietary_Restriction_DTO] = [Meal_Dietary_Restriction_DTO(
            meal_dietary_restriction_domain=x) for x in extended_meal_domain.dietary_restrictions]

    def serialize(self) -> dict:
        attribute_names = list(self.__dict__.keys())
        attributes = list(self.__dict__.values())
        serialized_attributes = super().serialize()
        for i in range(len(attributes)):
            if attribute_names[i] == "dietary_restrictions":
                serialized_attributes[attribute_names[i]] = [
                    x.serialize() for x in attributes[i]]
        return serialized_attributes
