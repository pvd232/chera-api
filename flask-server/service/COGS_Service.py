from domain.COGS_Domain import COGS_Domain
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from repository.COGS_Repository import COGS_Repository


class COGS_Service(object):
    def __init__(self, cogs_repository: "COGS_Repository") -> None:
        self.cogs_repository = cogs_repository

    def get_cogs(self) -> list[COGS_Domain]:
        return self.cogs_repository.get_cogs()

    def get_specific_cogs(
        self, num_meals, num_snacks: int, is_local: bool = False
    ) -> COGS_Domain:
        lcd_num_items = self.get_lcd_num_items(
            num_meals=num_meals, num_snacks=num_snacks
        )
        return COGS_Domain(
            cogs_object=self.cogs_repository.get_specific_cogs(
                num_items=lcd_num_items, is_local=is_local
            )
        )

    def get_num_items(self, num_meals: int, num_snacks: int) -> int:
        return int(num_meals + (num_snacks / 2))

    def get_num_boxes(self, num_meals: int, num_snacks: int) -> int:
        num_items = self.get_num_items(num_meals=num_meals, num_snacks=num_snacks)
        max_items_per_box = self.cogs_repository.get_cogs()[0].num_meals
        upper_bound = (max_items_per_box * 2) - 2
        if num_items > upper_bound:
            times_divisible = num_items // max_items_per_box
            remainder = num_items % max_items_per_box
            if remainder == 0:
                num_boxes = times_divisible
            else:
                num_boxes = times_divisible + 1
        elif num_items > max_items_per_box and num_items <= upper_bound:
            num_boxes = 2
        else:
            num_boxes = 1
        return int(num_boxes)

    # Get the lowest common denominator of meals and snacks (costs are calculated per meal, and are proportional to underlying num_meals range of 8-14)
    def get_lcd_num_items(self, num_meals: int, num_snacks: int) -> int:
        num_items = self.get_num_items(num_meals=num_meals, num_snacks=num_snacks)
        # Prepaid meals triggers no value for lcd_num_items
        # lcd_num_items = num_items
        max_items_per_box = self.cogs_repository.get_cogs()[0].num_meals
        upper_bound = (max_items_per_box * 2) - 2

        if num_items >= max_items_per_box and num_items <= upper_bound:
            lcd_num_items = num_items

        elif num_items > upper_bound:
            remainder = num_items % max_items_per_box
            lcd_num_items = max_items_per_box + remainder

        return int(lcd_num_items)

    def get_shipping_cost(
        self, num_meals: int, num_snacks: int, shipping_rate: float
    ) -> float:
        num_boxes = self.get_num_boxes(num_meals, num_snacks)
        shipping_cost = num_boxes * shipping_rate
        return shipping_cost

    def get_shipping_cost_per_meal(
        self, num_meals: int, num_snacks: int, shipping_rate: float
    ) -> float:
        shipping_cost = self.get_shipping_cost(
            num_meals=num_meals, num_snacks=num_snacks, shipping_rate=shipping_rate
        )
        return shipping_cost / self.get_num_items(
            num_meals=num_meals, num_snacks=num_snacks
        )

    def get_meal_cost(
        self, num_meals: int, num_snacks: int, shipping_rate: float
    ) -> float:
        associated_cogs = self.get_specific_cogs(
            num_meals=num_meals, num_snacks=num_snacks, is_local=False
        )
        shipping_cost_per_meal = self.get_shipping_cost_per_meal(
            num_meals=num_meals, num_snacks=num_snacks, shipping_rate=shipping_rate
        )
        meal_cost = associated_cogs.get_total_cost_per_meal() + shipping_cost_per_meal
        return meal_cost

    def get_meal_price(self, meal_cost: float) -> float:
        return float(round(meal_cost) + 1)

    def get_snack_price(self, meal_price: float) -> float:
        return meal_price / 2