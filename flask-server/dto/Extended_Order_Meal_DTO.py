from domain.Extended_Order_Meal_Domain import Extended_Order_Meal_Domain
from dto.Order_Meal_DTO import Order_Meal_DTO
from dto.Extended_Scheduled_Order_Meal_DTO import Extended_Scheduled_Order_Meal_DTO


class Extended_Order_Meal_DTO(Order_Meal_DTO):
    def __init__(self, extended_order_meal_domain: Extended_Order_Meal_Domain) -> None:
        super().__init__(order_meal_domain=extended_order_meal_domain)
        self.scheduled_order_meal: Extended_Scheduled_Order_Meal_DTO = Extended_Scheduled_Order_Meal_DTO(
            extended_scheduled_order_meal_domain=extended_order_meal_domain.scheduled_order_meal)
