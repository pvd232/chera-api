class Order_Calc_Service(object):
    def get_order_calc(
        self,
        num_items: int,
        meal_price: float,
        shipping_cost: float,
        discount_percentage: float = None,
    ) -> dict:
        service_fee = 0.0
        sales_tax_total = 0.0
        subtotal = meal_price * float(num_items)

        if discount_percentage:
            subtotal = subtotal * discount_percentage
        total = 0.0

        # no sales tax until 500K revenue
        sales_tax_percentage = 0
        sales_tax_total = 0
        total = subtotal + sales_tax_total
        service_fee = self.get_stripe_fee(total=total)

        return {
            "total": total,
            "subtotal": subtotal,
            "sales_tax_total": sales_tax_total,
            "stripe_fee_total": service_fee,
            "sales_tax_percentage": sales_tax_percentage,
            "shipping_total": shipping_cost,
        }

    def get_stripe_fee(self, total: float) -> float:
        return (0.029 * total) + 0.3

    def get_stripe_order_total(
        self,
        num_items: int,
        meal_price: float,
        discount_percentage: float = None,
    ) -> int:
        order_subtotal = float(num_items) * meal_price

        if discount_percentage:
            order_total = order_subtotal * discount_percentage
        else:
            order_total = order_subtotal

        stripe_order_total = int(order_total * 100)
        return stripe_order_total
