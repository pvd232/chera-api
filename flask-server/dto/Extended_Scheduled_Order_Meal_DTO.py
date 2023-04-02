from dto.Scheduled_Order_Meal_DTO import Scheduled_Order_Meal_DTO
from dto.Extended_Meal_DTO import Extended_Meal_DTO
from domain.Extended_Scheduled_Order_Meal_Domain import Extended_Scheduled_Order_Meal_Domain


class Extended_Scheduled_Order_Meal_DTO(Scheduled_Order_Meal_DTO):
    def __init__(self, extended_scheduled_order_meal_domain: 'Extended_Scheduled_Order_Meal_Domain') -> None:
        super().__init__(scheduled_order_meal_domain=extended_scheduled_order_meal_domain)
        self.associated_meal: Extended_Meal_DTO = Extended_Meal_DTO(
            extended_meal_domain=extended_scheduled_order_meal_domain.associated_meal)
