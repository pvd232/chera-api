import os
from pathlib import Path
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from typing import TYPE_CHECKING
from domain.Client_Domain import Client_Domain
from domain.Dietitian_Domain import Dietitian_Domain

if TYPE_CHECKING:
    from service.GCP_Secret_Manager_Service import GCP_Secret_Manager_Service
    from service.Date_Service import Date_Service
    from domain.Extended_Meal_Subscription_Invoice_Domain import (
        Extended_Meal_Subscription_Invoice_Domain,
    )
    from domain.FNCE_Lead_Domain import FNCE_Lead_Domain
    from domain.Staged_Client_Domain import Staged_Client_Domain


class Email_Service(object):
    def __init__(
        self, host_url, gcp_secret_manager_service: "GCP_Secret_Manager_Service"
    ) -> None:
        self.host = host_url
        self.theme_color = "#ffa40c"
        self.logo_url = (
            "https://storage.googleapis.com/meal-photos/bendito-small-updated.png"
        )
        self.mailgun_domain = "postmaster@info.bendito.io"
        self.mailgun_password = gcp_secret_manager_service.get_secret("MAILJET_PWD")

    def send_fnce_lead_email(self, fnce_lead: "FNCE_Lead_Domain") -> None:
        # creates SMTP
        s = smtplib.SMTP_SSL("smtp.gmail.com", 465)

        # Authentication
        s.login("peterdriscoll27@gmail.com", "jvuvmltffdxglfoq")

        # message to be sent
        message = "Message_you_need_to_send"

        # sending the mail
        s.sendmail("peterdriscoll27@gmail.com", fnce_lead.id, message)

        # terminating the session
        s.quit()

    def send_confirmation_email(
        self,
        user_type: str,
        user=None,
        delivery_date: datetime = None,
        tracking_url: str = None,
        date_service: "Date_Service" = None,
    ) -> None:
        if user_type == "Dietitian":
            email_file_name = (
                Path(".")
                .joinpath("flask-server")
                .joinpath("email_templates")
                .joinpath("dietitian_sign_up_confirmation.html")
            )
        else:
            email_file_name = (
                Path(".")
                .joinpath("flask-server")
                .joinpath("email_templates")
                .joinpath("client_sign_up_confirmation.html")
            )

        with open(email_file_name, "r") as mail_body:
            sender_address = "Welcome@info.bendito.io"
            email = user.id

            # Setup the MIME
            message = MIMEMultipart()
            message["From"] = sender_address
            message["To"] = email

            # The subject line
            message["Subject"] = "Welcome to Bendito - PLEASE READ"

            if user_type == "Client":
                mail_content = mail_body.read().format(
                    logo_url=self.logo_url,
                    theme_color=self.theme_color,
                    first_name=user.first_name.capitalize(),
                    delivery_month=date_service.months[delivery_date.month - 1],
                    delivery_day=delivery_date.day,
                    tracking_url=tracking_url,
                )
            else:
                mail_content = mail_body.read().format(
                    logo_url=self.logo_url, first_name=user.first_name.capitalize()
                )
            # The body and the attachments for the mail
            message.attach(MIMEText(mail_content, "html"))
            s = smtplib.SMTP("smtp.mailgun.org", 587)

            s.login(self.mailgun_domain, self.mailgun_password)
            s.sendmail(message["From"], message["To"], message.as_string())
            s.quit()

    def send_client_sign_up_notification_email(
        self,
        first_name: str,
        email: str,
        user_type: str,
        user: Client_Domain | Dietitian_Domain,
        env: str,
        zipcode: str = None,
    ) -> None:
        if user_type == "Staged_Client":
            email_file_name = (
                Path(".")
                .joinpath("flask-server")
                .joinpath("email_templates")
                .joinpath("client_sign_up_notification.html")
            )
        else:
            email_file_name = (
                Path(".")
                .joinpath("flask-server")
                .joinpath("email_templates")
                .joinpath("dietitian_sign_up_notification.html")
            )

        with open(email_file_name, "r") as mail_body:
            sender_address = "Growth@info.bendito.io"

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
        button_url = f"{self.host}/client-sign-up?staged_client_id={staged_client.id}"
        if staged_client.meals_prepaid:
            email_file_name = (
                Path(".")
                .joinpath("flask-server")
                .joinpath("email_templates")
                .joinpath("client_sign_up_prepaid_meals.html")
            )

        else:
            email_file_name = (
                Path(".")
                .joinpath("flask-server")
                .joinpath("email_templates")
                .joinpath("client_sign_up.html")
            )
        with open(email_file_name, "r") as mail_body:
            sender_address = "Registration@info.bendito.io"
            email = staged_client.id

            # Setup the MIME
            message = MIMEMultipart()
            message["From"] = sender_address
            message["To"] = email

            # The subject line
            if staged_client.meals_prepaid:
                message["Subject"] = "Claim Your Free Week of Meals"
            else:
                message["Subject"] = "Create your Bendito Account"

            mail_content = mail_body.read().format(
                logo_url=self.logo_url,
                theme_color=self.theme_color,
                first_name=staged_client.first_name.capitalize(),
                button_url=button_url,
            )
            # The body and the attachments for the mail
            message.attach(MIMEText(mail_content, "html"))
            s = smtplib.SMTP("smtp.mailgun.org", 587)
            # this password was generated ay the domain settings page on mailgun. its a really shitty confusing service.
            s.login(self.mailgun_domain, self.mailgun_password)
            s.sendmail(message["From"], message["To"], message.as_string())
            s.quit()

    def send_sign_up_reminder_email(
        self, staged_client: "Staged_Client_Domain"
    ) -> None:
        button_url = f"{self.host}/client-sign-up?staged_client_id={staged_client.id}"
        with open(
            "./flask-server/email_templates/client_sign_up_reminder.html", "r"
        ) as mail_body:
            sender_address = "Registration@info.bendito.io"
            email = staged_client.id

            # Setup the MIME
            message = MIMEMultipart()
            message["From"] = sender_address
            message["To"] = email

            # The subject line
            if staged_client.meals_prepaid:
                message["Subject"] = "Reminder - Claim Your Free Week of Meals"
            else:
                message["Subject"] = "Reminder - Create your Bendito Account"

            mail_content = mail_body.read().format(
                logo_url=self.logo_url,
                theme_color=self.theme_color,
                first_name=staged_client.first_name.capitalize(),
                button_url=button_url,
            )
            # The body and the attachments for the mail
            message.attach(MIMEText(mail_content, "html"))
            s = smtplib.SMTP("smtp.mailgun.org", 587)
            # this password was generated ay the domain settings page on mailgun. its a really shitty confusing service.
            s.login(self.mailgun_domain, self.mailgun_password)
            s.sendmail(message["From"], message["To"], message.as_string())
            s.quit()

    def send_password_reset_email(
        self, user: Client_Domain | Dietitian_Domain, domain: str
    ) -> None:
        button_url = f"{self.host}/reset-{domain}-password?{domain}_id={user.id}"
        with open(
            "./flask-server/email_templates/password_reset.html", "r"
        ) as mail_body:
            sender_address = "Password@info.bendito.io"
            email = user.id

            # Setup the MIME
            message = MIMEMultipart()
            message["From"] = sender_address
            message["To"] = email

            # The subject line
            message["Subject"] = "Reset Your Bendito Account Password"

            mail_content = mail_body.read().format(
                logo_url=self.logo_url,
                first_name=user.first_name.capitalize(),
                button_url=button_url,
                theme_color=self.theme_color,
            )

            # The body and the attachments for the mail
            message.attach(MIMEText(mail_content, "html"))
            s = smtplib.SMTP("smtp.mailgun.org", 587)
            # this password was generated ay the domain settings page on mailgun. its a really shitty confusing service.
            s.login(self.mailgun_domain, self.mailgun_password)
            s.sendmail(message["From"], message["To"], message.as_string())
            s.quit()

    def send_upcoming_deliveries_email(
        self,
        delivery_date: datetime,
        first_email_datetime: float,
        meal_subscription_invoices: list["Extended_Meal_Subscription_Invoice_Domain"],
        email_number: int,
    ) -> None:
        with open(
            "./flask-server/email_templates/upcoming_deliveries.html", "r"
        ) as mail_body:
            order_number = 0
            order_meal_text = ""
            for meal_subscription_invoice in meal_subscription_invoices:
                order_number += 1
                meal_dict = {}
                order_meal_text += f"<p style='font-size: 1rem;margin-bottom: 3vh;font-weight:bold;'>Order # {order_number} (Invoice Id {meal_subscription_invoice.id})</p>"
                for order_meal in meal_subscription_invoice.order_meals:
                    if email_number == 1 or (
                        email_number == 2
                        and order_meal.scheduled_order_meal.datetime
                        > first_email_datetime
                    ):
                        # set meal property such that order meal string function can output the formatted meal summary
                        if (
                            order_meal.scheduled_order_meal.associated_meal.id
                            not in meal_dict
                        ):
                            meal_dict[
                                order_meal.scheduled_order_meal.associated_meal.id
                            ] = order_meal.scheduled_order_meal.associated_meal
                        else:
                            meal_dict[
                                order_meal.scheduled_order_meal.associated_meal.id
                            ].quantity += 1
                for meal in meal_dict.values():
                    order_meal_text += str(meal)
            sender_address = "Delivery@info.bendito.io"

            # Setup the MIME
            message = MIMEMultipart()
            message["From"] = sender_address
            message["To"] = "patardriscoll@gmail.com"

            # The subject line
            message["Subject"] = (
                "Deliveries for the Week of "
                + delivery_date.strftime("%m/%d/%Y")
                + f" Email # {email_number}"
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
