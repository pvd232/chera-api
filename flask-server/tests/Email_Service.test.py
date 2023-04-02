import unittest
from datetime import datetime, timedelta, timezone
import uuid

# Add the root directory to sys.path
import sys
from pathlib import Path
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))

# Additionally remove the current file's directory from sys.path
try:
    sys.path.remove(str(parent))
except ValueError:  # Already removed
    pass

host_url = 'http://localhost:3000'


class AttrDict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

# 3/19/2022 Both first and second email passed tests


class Email_Service_Test(unittest.TestCase):
    # This test evaulates if the first email sent includes scheduled order meals created before the cutoff
    # This test also evaulates if the second email sent includes scheduled order meals created after the cutoff
    def send_upcoming_deliveries_email(self, email_number: int) -> None:
        from service.Email_Service import Email_Service
        from service.Date_Service import Date_Service
        from service.GCP_Secret_Manager_Service import GCP_Secret_Manager_Service

        meal_subscription_invoice_id = str(uuid.uuid4())
        meal_subscription_id = str(uuid.uuid4())
        subtotal = 100
        sales_tax_percentage = 0.08
        sales_tax_total = 8
        shipping_total = 10
        stripe_fee_total = 10
        stripe_invoice_id = str(uuid.uuid4())
        stripe_payment_intent_id = str(uuid.uuid4())
        total = 118

        first_email_datetime = Date_Service().get_first_email_datetime()
        meal_subscription_invoice_datetime = datetime.now(timezone.utc)
        meal_subscription_invoice_delivery_date = Date_Service().get_current_week_delivery_date()

        mock_order_meals = [
        ]

        # First email should only include 2 meals
        for i in range(2):
            mock_order_meals.append(AttrDict({
                "meal_id": uuid.uuid4(),
                "meal_subscription_invoice_id": meal_subscription_invoice_id,
                "scheduled_order_meal_id": uuid.uuid4(),
                "scheduled_order_meal": AttrDict({
                    # Datetime is before the cutoff
                    "datetime": first_email_datetime + timedelta(hours=-3),
                    "associated_meal": AttrDict({
                        "id": uuid.uuid4(),
                        "name": f"Meal {i}",
                        "description": f"Meal {i} description",
                        "price": i,
                        "image_url": f"https://meal-image-url-{i}.com",
                        "quantity": i
                    })
                })
            }))

        # Second email should only include 4 meals
        if email_number == 2:
            for i in range(4):
                mock_order_meals.append(AttrDict({
                    "meal_id": uuid.uuid4(),
                    "meal_subscription_invoice_id": meal_subscription_invoice_id,
                    "scheduled_order_meal_id": uuid.uuid4(),
                    "scheduled_order_meal": AttrDict({
                        # Datetime is after the cutoff
                        "datetime": first_email_datetime + timedelta(hours=3),
                        "associated_meal": AttrDict({
                            "id": uuid.uuid4(),
                            "name": f"Meal {i}",
                            "description": f"Meal {i} description",
                            "price": i,
                            "image_url": f"https://meal-image-url-{i}.com",
                            "quantity": i
                        })
                    })
                }))

        mock_meal_subscription_invoice = AttrDict({
            "id": meal_subscription_invoice_id,
            "meal_subscription_id": meal_subscription_id,
            "subtotal": subtotal,
            "sales_tax_percentage": sales_tax_percentage,
            "sales_tax_total": sales_tax_total,
            "shipping_total": shipping_total,
            "stripe_fee_total": stripe_fee_total,
            "stripe_invoice_id": stripe_invoice_id,
            "stripe_payment_intent_id": stripe_payment_intent_id,
            "total": total,
            "datetime": meal_subscription_invoice_datetime,
            "delivery_date": meal_subscription_invoice_delivery_date,
            "order_meals": mock_order_meals
        })

        Email_Service(host_url=host_url, gcp_secret_manager_service=GCP_Secret_Manager_Service()).send_upcoming_deliveries_email(delivery_date=meal_subscription_invoice_delivery_date,
                                                                                                                                 first_email_datetime=first_email_datetime, meal_subscription_invoices=[mock_meal_subscription_invoice], email_number=email_number)


# Email_Service_Test().send_upcoming_deliveries_email(email_number=1)
Email_Service_Test().send_upcoming_deliveries_email(email_number=2)
