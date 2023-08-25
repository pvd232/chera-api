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

        # Monday 2pm CST
        self.delivery_day_index = 0
        self.delivery_hour_index = 19

        # Saturday 10am CST
        self.shipping_day_index = 6
        self.shipping_hour_index = 15

        # Tuesday 10pm CST
        self.delivery_cutoff_day_index = 3
        self.delivery_cutoff_hour_index = 3

        self.sample_cutoff_hour_index = 11

        # Fri 6am CST
        self.normal_sample_cutoff_day_index = 4

        # Tues 6am CST
        self.alternate_sample_cutoff_day_index = 1

        # Batch with meals for the upcoming delivery date
        self.normal_sample_shipping_day_index = self.shipping_day_index
        self.normal_sample_shipping_hour_index = self.shipping_hour_index

        # Wed 10am CST
        self.alternate_sample_shipping_day_index = 2
        self.alternate_sample_shipping_hour_index = self.shipping_hour_index

        # Batch with meals for the upcoming delivery date
        self.normal_sample_delivery_day_index = self.delivery_day_index
        self.normal_sample_delivery_hour_index = self.delivery_hour_index

        # Fri 2pm CST
        self.alternate_sample_delivery_day_index = 4
        self.alternate_sample_delivery_hour_index = self.delivery_hour_index

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
        today_ = datetime.now(timezone.utc)
        today = datetime(
            year=today_.year,
            month=today_.month,
            day=today_.day,
            hour=self.delivery_hour_index,
            tzinfo=timezone.utc,
        )
        dd = today + timedelta((self.delivery_day_index - today.weekday() + 7) % 7)
        return dd.timestamp()

    def get_current_week_sample_delivery_date(self, today: datetime) -> float:
        today_wo_hour = datetime(
            year=today.year,
            month=today.month,
            day=today.day,
            hour=self.alternate_sample_delivery_hour_index,
            tzinfo=timezone.utc,
        )
        if (
            today.weekday() > self.normal_sample_cutoff_day_index
            or today.weekday() <= self.alternate_sample_cutoff_day_index
        ):
            dd = today_wo_hour + timedelta(
                (self.alternate_sample_delivery_day_index - today.weekday() + 7) % 7
            )
        else:
            dd = today_wo_hour + timedelta(
                (self.normal_sample_delivery_day_index - today.weekday() + 7) % 7
            )
        return dd.timestamp()

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

    def get_next_week_date(self, current_date: float) -> float:
        new_datetime = datetime.utcfromtimestamp(current_date).replace(
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

    def get_upcoming_delivery_dates(
        self, current_week_delivery_date: float
    ) -> list[float]:
        upcoming_delivery_dates = []
        for i in range(0, 4):
            upcoming_delivery_date = datetime.utcfromtimestamp(
                current_week_delivery_date
            ).replace(tzinfo=timezone.utc) + timedelta(days=i * 7)
            upcoming_delivery_dates.append(upcoming_delivery_date.timestamp())
        return upcoming_delivery_dates

    def get_upcoming_cutoff_delivery_dates(
        self, current_week_cutoff_date: float
    ) -> list[float]:
        upcoming_cutoff_delivery_dates = []
        for i in range(0, 4):
            upcoming_cutoff_date = datetime.utcfromtimestamp(
                current_week_cutoff_date
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
