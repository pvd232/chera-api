import unittest
from datetime import datetime, timezone, timedelta

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


class Date_Service(unittest.TestCase):
    def get_current_week_delivery_date(self) -> None:
        from service.Date_Service import Date_Service

        test_datetime = datetime.utcfromtimestamp(
            int(Date_Service().get_current_week_delivery_date())
        ).replace(tzinfo=timezone.utc)

        # Update this to be the upcoming delivery date
        self.assertEqual(
            test_datetime, datetime(2023, 3, 27, 19, 0, tzinfo=timezone.utc)
        )
        self.assertTrue(test_datetime.tzname() == "UTC")
        self.assertTrue(test_datetime.timestamp() > datetime.utcnow().timestamp())

    def get_current_week_sample_delivery_date(
        self, today: datetime, expected_delivery_date: datetime
    ) -> None:
        from service.Date_Service import Date_Service

        test_datetime = datetime.utcfromtimestamp(
            int(Date_Service().get_current_week_sample_delivery_date(today=today))
        ).replace(tzinfo=timezone.utc)

        # Update this to be the upcoming delivery date
        self.assertEqual(test_datetime, expected_delivery_date)
        self.assertTrue(test_datetime.tzname() == "UTC")
        self.assertTrue(test_datetime.timestamp() > datetime.utcnow().timestamp())

    def get_current_week_cutoff(self) -> None:
        from service.Date_Service import Date_Service

        test_datetime = datetime.utcfromtimestamp(
            Date_Service().get_current_week_cutoff(
                current_delivery_date=Date_Service().get_current_week_delivery_date()
            )
        ).replace(tzinfo=timezone.utc)

        self.assertEqual(
            test_datetime,
            datetime.utcfromtimestamp(
                Date_Service().get_current_week_delivery_date()
            ).replace(tzinfo=timezone.utc)
            - timedelta(
                days=Date_Service().delivery_cutoff_day_difference,
                hours=Date_Service().delivery_cutoff_hour_difference,
            ),
        )
        self.assertTrue(test_datetime.tzname() == "UTC")

    def get_stripe_delivery_date_anchor(self) -> None:
        from service.Date_Service import Date_Service

        test_datetime = datetime.utcfromtimestamp(
            Date_Service().get_stripe_delivery_date_anchor()
        ).replace(tzinfo=timezone.utc)
        current_week_cutoff = datetime.utcfromtimestamp(
            Date_Service().get_current_week_cutoff(
                current_delivery_date=Date_Service().get_current_week_delivery_date()
            )
        ).replace(tzinfo=timezone.utc)
        if current_week_cutoff.timestamp() < datetime.utcnow().timestamp():
            # Update this to be the upcoming delivery date
            self.assertEqual(
                test_datetime,
                datetime.utcfromtimestamp(
                    Date_Service().get_current_week_cutoff(
                        current_delivery_date=Date_Service().get_current_week_delivery_date()
                    )
                ).replace(tzinfo=timezone.utc)
                + timedelta(days=7),
            )
        else:
            self.assertEqual(
                test_datetime,
                datetime.utcfromtimestamp(
                    Date_Service().get_current_week_cutoff(
                        current_delivery_date=Date_Service().get_current_week_delivery_date()
                    )
                ).replace(tzinfo=timezone.utc),
            )

        self.assertTrue(test_datetime.tzname() == "UTC")
        self.assertIsInstance(test_datetime, datetime)

        stripe_timestamp_int = int(test_datetime.timestamp())
        self.assertIsInstance(stripe_timestamp_int, int)
        self.assertTrue(test_datetime.timestamp() > datetime.utcnow().timestamp())

    def get_next_week_delivery_date(self) -> None:
        from service.Date_Service import Date_Service

        test_timestamp = Date_Service().get_current_week_delivery_date()
        test_datetime = datetime.utcfromtimestamp(test_timestamp).replace(
            tzinfo=timezone.utc
        )
        test_next_week_delivery_date = datetime.utcfromtimestamp(
            Date_Service().get_next_week_delivery_date(
                current_delivery_date=test_timestamp
            )
        ).replace(tzinfo=timezone.utc)

        self.assertEqual(
            test_next_week_delivery_date, test_datetime + timedelta(days=7)
        )
        self.assertTrue(test_next_week_delivery_date.tzname() == "UTC")
        self.assertTrue(test_datetime.timestamp() > datetime.utcnow().timestamp())

    def get_shipping_date_from_delivery_date(self) -> None:
        from service.Date_Service import Date_Service

        current_delivery_date = datetime.utcfromtimestamp(
            Date_Service().get_current_week_delivery_date()
        ).replace(tzinfo=timezone.utc)
        test_datetime = datetime.utcfromtimestamp(
            Date_Service().get_shipping_date_from_delivery_date(
                current_delivery_date=current_delivery_date
            )
        ).replace(tzinfo=timezone.utc)

        # Update this to the difference between the current delivery date and the shipping date
        self.assertEqual(
            test_datetime,
            current_delivery_date
            - timedelta(
                days=Date_Service().delivery_shipping_day_difference,
                hours=Date_Service().delivery_shipping_hour_difference,
            ),
        )
        self.assertTrue(test_datetime.tzname() == "UTC")


# Date_Service().get_current_week_delivery_date()
# Date_Service().get_current_week_cutoff()
# Date_Service().get_stripe_delivery_date_anchor()
# Date_Service().get_next_week_delivery_date()
# Date_Service().get_shipping_date_from_delivery_date()
# Date_Service().get_shipping_date_from_delivery_date()
Date_Service().get_current_week_sample_delivery_date(
    today=datetime.now(timezone.utc),
    expected_delivery_date=datetime(2023, 7, 17, 19, 0, tzinfo=timezone.utc),
)
Date_Service().get_current_week_sample_delivery_date(
    today=datetime.now(timezone.utc) + timedelta(days=2),
    expected_delivery_date=datetime(2023, 7, 21, 19, 0, tzinfo=timezone.utc),
)
Date_Service().get_current_week_sample_delivery_date(
    today=datetime.now(timezone.utc) + timedelta(days=4),
    expected_delivery_date=datetime(2023, 7, 21, 19, 0, tzinfo=timezone.utc),
)
Date_Service().get_current_week_sample_delivery_date(
    today=datetime.now(timezone.utc) + timedelta(days=6),
    expected_delivery_date=datetime(2023, 7, 24, 19, 0, tzinfo=timezone.utc),
)
