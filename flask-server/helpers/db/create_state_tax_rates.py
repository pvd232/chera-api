from flask_sqlalchemy import SQLAlchemy
import stripe
from models import State_Sales_Tax_Model


def create_state_tax_rates(db: SQLAlchemy) -> None:
    # had to round NY state sales tax from 0.08875 to 0.0888 for stripe
    states = [
        {"state": "NJ", "sales_tax": 0.0625},
        {"state": "NY", "sales_tax": 0.08875},
    ]
    for state in states:
        state_name = state["state"]
        # stripe expects tax rates to be inputted as percentages
        stripe_state_sales_tax_percentage = state["sales_tax"] * 100
        state_sales_tax_percentage = state["sales_tax"]

        stripe_state_tax_rate = stripe.TaxRate.create(
            display_name=f"{state_name} Sales Tax",
            inclusive=False,
            percentage=stripe_state_sales_tax_percentage,
        )

        new_state_sales_tax = State_Sales_Tax_Model(
            state=state_name,
            sales_tax_percentage=state_sales_tax_percentage,
            stripe_tax_id=stripe_state_tax_rate.id,
        )

        db.session.add(new_state_sales_tax)
    db.session.commit()
