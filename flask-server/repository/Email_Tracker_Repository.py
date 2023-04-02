from repository.Base_Repository import Base_Repository
from models import Email_Tracker_Model
from datetime import date


class Email_Tracker_Repository(Base_Repository):
    def check_email_sent(self, todays_date: date) -> bool:
        email_status = self.db.session.query(Email_Tracker_Model).filter(
            Email_Tracker_Model.date_email_sent == todays_date)
        if email_status:
            return True
        else:
            return False

    def update_email_sent(self, todays_date: date) -> None:
        new_email_date = Email_Tracker_Model(date_email_sent=todays_date)
        self.db.session.add(new_email_date)
        self.db.session.commit()
