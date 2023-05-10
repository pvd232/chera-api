from datetime import datetime, timezone, timedelta


class Date_Service(object):
    def __init__(self) -> None:
        self.months = [
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December",
        ]
        self.days = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ]

        # Delivery times are in UTC (CST + 5)
        self.delivery_day_index = 0
        self.delivery_hour_index = 19
        self.shipping_day_index = 5
        self.shipping_hour_index = 16
        self.delivery_cutoff_day_index = 3
        self.delivery_cutoff_hour_index = 3
        self.first_email_day_index = self.delivery_cutoff_day_index
        self.first_email_hour_index = 12
        self.first_email_cutoff_difference = (
            self.delivery_cutoff_hour_index - self.first_email_hour_index
        )
        self.second_email_day_index = self.delivery_cutoff_day_index
        self.second_email_hour_index = self.delivery_cutoff_hour_index + 1

        # Compute the difference by subtracting the delivery day index from the shipping day index
        # The upcoming delivery date is independent, while the shipping date is dependent on the delivery date
        if self.delivery_day_index > self.shipping_day_index:
            self.delivery_shipping_day_difference = (
                self.delivery_day_index - self.shipping_day_index
            )
        else:
            self.delivery_shipping_day_difference = (
                self.delivery_day_index + 7
            ) - self.shipping_day_index
        self.delivery_shipping_hour_difference = (
            self.delivery_hour_index - self.shipping_hour_index
        )

        # The upcoming delivery date is independent, while the delivery cutoff date is dependent on the delivery date
        if self.delivery_day_index > self.delivery_cutoff_day_index:
            self.delivery_cutoff_day_difference = (
                self.delivery_day_index - self.delivery_cutoff_day_index
            )

        else:
            self.delivery_cutoff_day_difference = (
                self.delivery_day_index + 7
            ) - self.delivery_cutoff_day_index
        self.delivery_cutoff_hour_difference = (
            self.delivery_hour_index - self.delivery_cutoff_hour_index
        )

    def get_current_week_delivery_date(self) -> float:
        today = datetime.now(timezone.utc)
        days_until_delivery_day = self.delivery_day_index - today.weekday()
        hours_until_delivery_day = self.delivery_hour_index - today.hour
        if days_until_delivery_day < 0 or (
            days_until_delivery_day == 0 and hours_until_delivery_day <= 0
        ):
            days_until_delivery_day += 7
        current_week_delivery_date = datetime(
            year=today.year,
            month=today.month,
            day=today.day,
            hour=self.delivery_hour_index,
            tzinfo=timezone.utc,
        ) + timedelta(days=days_until_delivery_day)
        return current_week_delivery_date.timestamp()

    def get_current_week_cutoff(self, current_delivery_date: float) -> float:
        current_delivery_datetime = datetime.utcfromtimestamp(
            current_delivery_date
        ).replace(tzinfo=timezone.utc)
        current_week_cutoff = datetime(
            year=current_delivery_datetime.year,
            month=current_delivery_datetime.month,
            day=current_delivery_datetime.day,
            hour=current_delivery_datetime.hour,
            tzinfo=timezone.utc,
        ) - timedelta(
            days=self.delivery_cutoff_day_difference,
            hours=self.delivery_cutoff_hour_difference,
        )
        return current_week_cutoff.timestamp()

    def get_stripe_delivery_date_anchor(self) -> float:
        today = datetime.now(timezone.utc)
        current_week_anchor = datetime.utcfromtimestamp(
            self.get_current_week_cutoff(
                current_delivery_date=self.get_current_week_delivery_date()
            )
        ).replace(tzinfo=timezone.utc)
        # If the day is wednesday or later then the anchor is next week
        if today.timestamp() >= current_week_anchor.timestamp():
            current_week_anchor += timedelta(days=7)
        return current_week_anchor.timestamp()

    def get_next_week_delivery_date(self, current_delivery_date: float) -> float:
        new_datetime = datetime.utcfromtimestamp(current_delivery_date).replace(
            tzinfo=timezone.utc
        ) + timedelta(days=7)
        return new_datetime.timestamp()

    def get_shipping_date_from_delivery_date(
        self, current_delivery_date: float
    ) -> float:
        shipping_date = datetime(
            year=current_delivery_date.year,
            month=current_delivery_date.month,
            day=current_delivery_date.day,
            hour=current_delivery_date.hour,
            tzinfo=timezone.utc,
        ) - timedelta(
            days=self.delivery_shipping_day_difference,
            hours=self.delivery_shipping_hour_difference,
        )
        return shipping_date.timestamp()

    def get_upcoming_delivery_dates(self) -> list[float]:
        upcoming_delivery_dates = []
        current_delivery_date = self.get_current_week_delivery_date()
        for i in range(0, 4):
            upcoming_delivery_date = datetime.utcfromtimestamp(
                current_delivery_date
            ).replace(tzinfo=timezone.utc) + timedelta(days=i * 7)
            upcoming_delivery_dates.append(upcoming_delivery_date.timestamp())
        return upcoming_delivery_dates

    def get_upcoming_cutoff_delivery_dates(self) -> list[float]:
        upcoming_cutoff_delivery_dates = []
        current_delivery_date = self.get_current_week_delivery_date()
        for i in range(0, 4):
            upcoming_cutoff_date = datetime.utcfromtimestamp(
                self.get_current_week_cutoff(
                    current_delivery_date=current_delivery_date
                )
            ).replace(tzinfo=timezone.utc) + timedelta(days=i * 7)
            upcoming_cutoff_delivery_dates.append(upcoming_cutoff_date.timestamp())
        return upcoming_cutoff_delivery_dates

    def get_first_email_datetime(self) -> float:
        current_week_cutoff = self.get_current_week_cutoff(
            current_delivery_date=self.get_current_week_delivery_date()
        )
        first_email_datetime = datetime.utcfromtimestamp(current_week_cutoff).replace(
            tzinfo=timezone.utc
        ) + timedelta(hours=self.first_email_cutoff_difference)
        # Cutoff day is the same as the first email day
        return first_email_datetime
