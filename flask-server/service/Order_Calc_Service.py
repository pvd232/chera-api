class Order_Calc_Service(object):
    def get_order_calc(
        self,
        num_meals: int,
        num_snacks: int,
        meal_price: float,
        snack_price: float,
        shipping_cost: float,
        discount_percentage: float = None,
    ) -> dict:
        service_fee = 0.0
        sales_tax_total = 0.0
        meals_subtotal = meal_price * float(num_meals)
        snacks_subtotal = snack_price * float(num_snacks)
        if discount_percentage:
            meals_subtotal = meals_subtotal * discount_percentage
            snacks_subtotal = snacks_subtotal * discount_percentage
        total = 0.0

        # no sales tax until 500K revenue
        sales_tax_percentage = 0
        sales_tax_total = 0
        total = meals_subtotal + sales_tax_total + snacks_subtotal + shipping_cost
        service_fee = self.get_stripe_fee(total=total)

        return {
            "total": total,
            "subtotal": meals_subtotal,
            "sales_tax_total": sales_tax_total,
            "stripe_fee_total": service_fee,
            "sales_tax_percentage": sales_tax_percentage,
            "shipping_total": shipping_cost,
        }

    def get_stripe_fee(self, total: float) -> float:
        return (0.029 * total) + 0.3

    def get_stripe_order_total(
        self,
        num_meals: int,
        num_snacks: int,
        meal_price: float,
        snack_price: float,
        shipping_cost: float,
        discount_percentage: float = None,
    ) -> int:
        order_subtotal = float(num_meals) * meal_price
        order_subtotal += float(num_snacks) * snack_price

        if discount_percentage:
            order_subtotal = order_subtotal * discount_percentage

        order_total = order_subtotal + shipping_cost
        stripe_order_total = int(order_total * 100)
        return stripe_order_total
