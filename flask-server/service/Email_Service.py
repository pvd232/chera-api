from pathlib import Path
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from domain.Client_Domain import Client_Domain
from domain.Dietitian_Domain import Dietitian_Domain
from flask import request
from typing import TYPE_CHECKING
from typing import Optional

if TYPE_CHECKING:
    from service.GCP_Secret_Manager_Service import GCP_Secret_Manager_Service
    from domain.Extended_Meal_Subscription_Invoice_Domain import (
        Extended_Meal_Subscription_Invoice_Domain,
    )
    from domain.Extended_Meal_Email_Summary_Domain import (
        Extended_Meal_Email_Summary_Domain,
    )
    from domain.FNCE_Lead_Domain import FNCE_Lead_Domain
    from domain.Staged_Client_Domain import Staged_Client_Domain


class Email_Service(object):
    def __init__(
        self, gcp_secret_manager_service: "GCP_Secret_Manager_Service"
    ) -> None:
        self.host = request.host
        self.scheme = request.scheme
        self.theme_color = "#ffa40c"
        self.logo_url = (
            "https://storage.googleapis.com/chera_logo/chera_logo_300x300.png"
        )
        self.mailgun_domain = "postmaster@support.cherahealth.com"
        self.mailgun_password = gcp_secret_manager_service.get_secret(
            "MAILGUN_PASSWORD"
        )
        self.template_email_file = Path(".", "email_templates", "template.html")

        if self.scheme == "http":
            self.frontend_host = "localhost:3000"

    def send_fnce_lead_email(self, fnce_lead: "FNCE_Lead_Domain") -> None:
        # creates SMTP
        s = smtplib.SMTP_SSL("smtp.gmail.com", 465)

        # Authentication
        s.login("peterdriscoll@cherahealth.com", "hmdisbafknqnblst")

        calendly_link = (
            "https://calendly.com/peterdriscoll-chera/chera-swe-internship-interview"
        )

        # sending the mail
        s.sendmail("peterdriscoll@cherahealth.com", fnce_lead.id, calendly_link)
        # terminating the session
        s.quit()

    def send_recruiting_email(
        self,
        first_name: str,
        email: str,
        role: str,
        calendly_link: str,
        testing: bool,
        file_name: str,
    ) -> None:
        # creates SMTP
        s = smtplib.SMTP_SSL("smtp.gmail.com", 465)

        # Authentication
        s.login("peterdriscoll@cherahealth.com", "hmdisbafknqnblst")

        email_file_name = (
            Path(".")
            .joinpath("email_templates")
            .joinpath("internship_interview")
            .joinpath(f"{file_name}.html")
        )

        with open(email_file_name, "r") as mail_body:
            # Setup the MIME
            message = MIMEMultipart()
            message["From"] = "peterdriscoll@cherahealth.com"
            if not testing:
                message["To"] = email
            else:
                message["To"] = message["From"]

            # The subject line
            message["Subject"] = f"Chera {role} Internship Interview"

            mail_content = mail_body.read().format(
                first_name=first_name, role=role, calendly_link=calendly_link
            )
            # The body and the attachments for the mail
            message.attach(MIMEText(mail_content, "html"))
            # sending the mail

            s.sendmail(message["From"], message["To"], message.as_string())

            # terminating the session
            s.quit()

    def send_pause_recruiting_email(
        self,
        first_name: str,
        email: str,
        testing: bool,
    ) -> None:
        # creates SMTP
        s = smtplib.SMTP_SSL("smtp.gmail.com", 465)

        # Authentication
        s.login("peterdriscoll@cherahealth.com", "hmdisbafknqnblst")

        email_file_name = (
            Path(".")
            .joinpath("email_templates")
            .joinpath("internship_interview")
            .joinpath("pause_hiring.html")
        )

        with open(email_file_name, "r") as mail_body:
            # Setup the MIME
            message = MIMEMultipart()
            message["From"] = "peterdriscoll@cherahealth.com"
            if not testing:
                message["To"] = email
            else:
                message["To"] = message["From"]

            # The subject line
            message["Subject"] = f"Chera Hiring Pause"

            mail_content = mail_body.read().format(first_name=first_name)
            # The body and the attachments for the mail
            message.attach(MIMEText(mail_content, "html"))
            # sending the mail

            s.sendmail(message["From"], message["To"], message.as_string())

            # terminating the session
            s.quit()

    def send_hiring_status_update_email(
        self,
        first_name: str,
        email: str,
        testing: bool,
    ) -> None:
        # creates SMTP
        s = smtplib.SMTP_SSL("smtp.gmail.com", 465)

        # Authentication
        s.login("peterdriscoll@cherahealth.com", "hmdisbafknqnblst")

        email_file_name = (
            Path(".")
            .joinpath("email_templates")
            .joinpath("internship_interview")
            .joinpath("hiring_status_update.html")
        )

        with open(email_file_name, "r") as mail_body:
            # Setup the MIME
            message = MIMEMultipart()
            message["From"] = "peterdriscoll@cherahealth.com"
            if not testing:
                message["To"] = email
            else:
                message["To"] = message["From"]

            # The subject line
            message["Subject"] = f"Chera Internship Status Update"

            mail_content = mail_body.read().format(first_name=first_name)
            # The body and the attachments for the mail
            message.attach(MIMEText(mail_content, "html"))
            # sending the mail

            s.sendmail(message["From"], message["To"], message.as_string())

            # terminating the session
            s.quit()

    def send_offer_notification_email(
        self,
        first_name: str,
        email: str,
        role: str,
        email_file_name: str,
        testing: bool,
    ) -> None:
        # creates SMTP
        s = smtplib.SMTP_SSL("smtp.gmail.com", 465)

        # Authentication
        s.login("peterdriscoll@cherahealth.com", "hmdisbafknqnblst")

        email_file_name = (
            Path(".")
            .joinpath("email_templates")
            .joinpath("internship_interview")
            .joinpath(email_file_name)
        )

        with open(email_file_name, "r") as mail_body:
            # Setup the MIME
            message = MIMEMultipart()
            message["From"] = "peterdriscoll@cherahealth.com"
            if not testing:
                message["To"] = email
            else:
                message["To"] = message["From"]

            # The subject line
            message["Subject"] = f"Chera {role} Internship Offer"

            mail_content = mail_body.read().format(first_name=first_name, role=role)
            # The body and the attachments for the mail
            message.attach(MIMEText(mail_content, "html"))
            # sending the mail

            s.sendmail(message["From"], message["To"], message.as_string())

            # terminating the session
            s.quit()

    def send_confirmation_email(
        self,
        user_type: str,
        user: Optional[Client_Domain | Dietitian_Domain] = None,
        delivery_date: datetime = None,
        cutoff_date: datetime = None,
        tracking_url: str = None,
    ) -> None:
        delivery_instructions = "Look for a plain white box, 1 foot tall."
        email_file_name = Path(".").joinpath(
            "email_templates", user_type.lower(), "sign_up_confirmation.html"
        )
        if user_type == "Client":
            mail_content = email_file_name.read_text().format(
                delivery_instructions=delivery_instructions,
                delivery_day=delivery_date.strftime("%A"),
                delivery_month=delivery_date.strftime("%B"),
                delivery_date=delivery_date.day,
                cutoff_day=cutoff_date.strftime("%A"),
                cutoff_time=cutoff_date.strftime("%I:%M %p %Z"),
                tracking_url=tracking_url,
            )
        else:
            mail_content = email_file_name.read_text()

        complete_email = self.template_email_file.read_text().format(
            logo_url=self.logo_url,
            first_name=user.first_name.capitalize(),
            content=mail_content,
        )
        # The body and the attachments for the mail
        sender_address = "Chera@support.cherahealth.com"
        email = user.id

        # Setup the MIME
        message = MIMEMultipart()
        message["From"] = sender_address
        message["To"] = email

        # The subject line
        message["Subject"] = "Welcome to Chera - Your First Delivery is on the Way!"
        message.attach(MIMEText(complete_email, "html"))
        s = smtplib.SMTP("smtp.mailgun.org", 587)

        s.login(self.mailgun_domain, self.mailgun_password)
        s.sendmail(message["From"], message["To"], message.as_string())
        s.quit()

    def send_new_user_sign_up_notification(
        self,
        first_name: str,
        email: str,
        user_type: str,
        user: Client_Domain | Dietitian_Domain,
        env: str,
        zipcode: str = None,
    ) -> None:
        if user_type == "Client" or user_type == "Staged_Client":
            email_template_name = "client_sign_up_notification.html"
        else:
            email_template_name = "dietitian_sign_up_notification.html"

        email_file_name = (
            Path(".")
            .joinpath("email_templates")
            .joinpath("admin")
            .joinpath(email_template_name)
        )

        with open(email_file_name, "r") as mail_body:
            sender_address = "Chera@support.cherahealth.com"

            # Setup the MIME
            message = MIMEMultipart()
            message["From"] = sender_address
            message["To"] = email

            if env == "debug":
                subject_message = f"TESTING New {user_type} Account"
            else:
                subject_message = f"New {user_type} Account"

            message["Subject"] = subject_message  # The subject line

            if user_type == "Staged_Client":
                mail_content = mail_body.read().format(
                    logo_url=self.logo_url,
                    first_name=first_name,
                    user_type=user_type,
                    user_first_name=user.first_name.capitalize(),
                    email=user.id,
                )
            else:
                mail_content = mail_body.read().format(
                    logo_url=self.logo_url,
                    first_name=first_name,
                    user_type=user_type,
                    user_first_name=user.first_name.capitalize(),
                    user_last_name=user.last_name.capitalize(),
                    email=user.id,
                    zipcode=zipcode,
                )

            # The body and the attachments for the mail
            message.attach(MIMEText(mail_content, "html"))
            s = smtplib.SMTP("smtp.mailgun.org", 587)
            # this password was generated ay the domain settings page on mailgun. its a really shitty confusing service.
            s.login(self.mailgun_domain, self.mailgun_password)
            s.sendmail(message["From"], message["To"], message.as_string())
            s.quit()

    def send_sign_up_email(self, staged_client: "Staged_Client_Domain") -> None:
        button_url = f"{self.scheme}://{self.host}/client_sign_up/{staged_client.id}"
        if staged_client.meals_prepaid:
            email_template_name = "sign_up_prepaid_meals.html"
        else:
            email_template_name = "sign_up.html"
        sign_up_button = (
            Path(".", "email_templates", "round_button.html")
            .read_text()
            .format(
                button_url=button_url,
                button_text="Create account",
            )
        )
        mail_content = (
            Path(".", "email_templates", "client", email_template_name)
            .read_text()
            .format(
                sign_up_button=sign_up_button,
            )
        )

        complete_email = self.template_email_file.read_text().format(
            logo_url=self.logo_url,
            first_name=staged_client.first_name.capitalize(),
            content=mail_content,
        )

        sender_address = "Chera@support.cherahealth.com"
        email = staged_client.id

        # Setup the MIME
        message = MIMEMultipart()
        message["From"] = sender_address
        message["To"] = email

        # The subject line
        if staged_client.meals_prepaid:
            message["Subject"] = "Claim Your Free Week of Meals"
        else:
            message["Subject"] = "Create your Chera Account"

        # The body and the attachments for the mail
        message.attach(MIMEText(complete_email, "html"))
        s = smtplib.SMTP("smtp.mailgun.org", 587)
        # this password was generated ay the domain settings page on mailgun. its a really shitty confusing service.
        s.login(self.mailgun_domain, self.mailgun_password)
        s.sendmail(message["From"], message["To"], message.as_string())
        s.quit()

    def send_sign_up_reminder_email(
        self, staged_client: "Staged_Client_Domain"
    ) -> None:
        button_url = f"{self.scheme}://{self.host}/client_sign_up/{staged_client.id}"
        sign_up_button = (
            Path(".")
            .joinpath("email_templates", "round_button.html")
            .read_text()
            .format(button_url=button_url, button_text="Create account")
        )
        mail_content = (
            Path(".")
            .joinpath("email_templates", "client", "sign_up_reminder.html")
            .read_text()
            .format(
                first_name=staged_client.first_name.capitalize(),
                sign_up_button=sign_up_button,
            )
        )
        complete_email = self.template_email_file.read_text().format(
            logo_url=self.logo_url,
            first_name=staged_client.first_name.capitalize(),
            content=mail_content,
        )

        sender_address = "Chera@support.cherahealth.com"
        email = staged_client.id

        # Setup the MIME
        message = MIMEMultipart()
        message["From"] = sender_address

        message["To"] = email

        # The subject line
        if staged_client.meals_prepaid:
            message["Subject"] = "Reminder - Claim Your Prepaid First Week of Meals"
        else:
            message["Subject"] = "Reminder - Create Your Chera Account"
        # The body and the attachments for the mail
        message.attach(MIMEText(complete_email, "html"))
        s = smtplib.SMTP("smtp.mailgun.org", 587)
        # this password was generated ay the domain settings page on mailgun. its a really shitty confusing service.
        s.login(self.mailgun_domain, self.mailgun_password)
        s.sendmail(message["From"], message["To"], message.as_string())
        s.quit()

    # def send_password_reset_email(
    #     self,
    #     user: Client_Domain | Dietitian_Domain,
    #     domain: str,
    #     gcp_secret_manager_service: "GCP_Secret_Manager_Service",
    # ) -> None:
    #     import jwt
    #     from time import time
    #     import os

    #     # Create an encrypted expiration timestamp using 30 minutes from now
    #     expires_in = 30 * 60
    #     pwd_token = jwt.encode(
    #         {"reset_password": user.id, "exp": time() + expires_in},
    #         os.environ.get(
    #             "JWT_SECRET", gcp_secret_manager_service.get_secret("JWT_SECRET")
    #         ),
    #         algorithm="HS256",
    #     )
    #     # Append the expiration timestamp to the reset link
    #     if self.env == "debug":
    #         button_url = f"https://cherahealth.com"
    #     else:
    #         button_url = f"{self.frontend_host}/reset-{domain}-password?{domain}_id={user.id}&reset_password_token={pwd_token.decode('utf-8')}"
    #     reset_password_button = (
    #         Path(".")
    #         .joinpath("email_templates", "round_button.html")
    #         .read_text()
    #         .format(button_url=button_url, button_text="Reset password")
    #     )
    #     mail_content = (
    #         Path(".")
    #         .joinpath("email_templates", "password_reset_request.html")
    #         .read_text()
    #         .format(
    #             reset_password_button=reset_password_button,
    #             user_email=user.id,
    #         )
    #     )
    #     complete_email = self.template_email_file.read_text().format(
    #         logo_url=self.logo_url,
    #         first_name=user.first_name.capitalize(),
    #         content=mail_content,
    #     )

    #     sender_address = "Chera@support.cherahealth.com"
    #     email = user.id

    #     # Setup the MIME
    #     message = MIMEMultipart()
    #     message["From"] = sender_address
    #     message["To"] = email

    #     # The subject line
    #     message["Subject"] = "Reset Your Chera Password"

    #     # The body and the attachments for the mail
    #     message.attach(MIMEText(complete_email, "html"))
    #     s = smtplib.SMTP("smtp.mailgun.org", 587)
    #     # this password was generated ay the domain settings page on mailgun. its a really shitty confusing service.
    #     s.login(self.mailgun_domain, self.mailgun_password)
    #     s.sendmail(message["From"], message["To"], message.as_string())
    #     s.quit()

    def send_upcoming_deliveries_email(
        self,
        delivery_date: datetime,
        meal_subscription_invoices: list["Extended_Meal_Subscription_Invoice_Domain"],
    ) -> None:
        email_file_name = (
            Path(".")
            .joinpath("email_templates")
            .joinpath("admin")
            .joinpath("upcoming_deliveries.html")
        )
        with open(email_file_name, "r") as mail_body:
            order_number = 0
            order_meal_text = ""
            for meal_subscription_invoice in meal_subscription_invoices:
                order_number += 1
                meal_dict: dict[str, "Extended_Meal_Email_Summary_Domain"] = {}
                order_meal_text += f"<p style='font-size: 1rem;margin-bottom: 3vh;font-weight:bold;'>Order # {order_number} (Invoice Id {meal_subscription_invoice.id})</p>"
                for order_meal in meal_subscription_invoice.order_meals:
                    # Set meal property such that order meal string function can output the formatted meal summary
                    if order_meal.associated_meal.id not in meal_dict:
                        meal_dict[
                            order_meal.associated_meal.id
                        ] = order_meal.associated_meal
                    else:
                        meal_dict[order_meal.associated_meal.id].quantity += 1
                for meal in meal_dict.values():
                    order_meal_text += str(meal)
            sender_address = "Chera@support.cherahealth.com"

            # Setup the MIME
            message = MIMEMultipart()
            message["From"] = sender_address
            message["To"] = "peterdriscoll@cherahealth.com"

            # The subject line
            message["Subject"] = "Deliveries for the Week of " + delivery_date.strftime(
                "%m/%d/%Y"
            )

            mail_content = mail_body.read().format(
                logo_url=self.logo_url,
                delivery_date=delivery_date.strftime("%m/%d/%Y"),
                order_meal_text=order_meal_text,
            )

            # The body and the attachments for the mail
            message.attach(MIMEText(mail_content, "html"))
            s = smtplib.SMTP("smtp.mailgun.org", 587)
            # this password was generated ay the domain settings page on mailgun. its a really shitty confusing service.
            s.login(self.mailgun_domain, self.mailgun_password)
            s.sendmail(message["From"], message["To"], message.as_string())
            s.quit()
