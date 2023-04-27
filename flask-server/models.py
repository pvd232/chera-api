from service.GCP_Secret_Manager_Service import GCP_Secret_Manager_Service
from dotenv import load_dotenv
import json
import uuid
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy.dialects.postgresql import UUID
import os
from sqlalchemy.schema import DropTable, CheckConstraint
from sqlalchemy.ext.compiler import compiles
from werkzeug.security import generate_password_hash
import stripe
import shippo
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from domain.Meal_Domain import Meal_Domain
    from domain.Meal_Plan_Meal_Domain import Meal_Plan_Meal_Domain
    from domain.Meal_Dietary_Restriction_Domain import Meal_Dietary_Restriction_Domain
    from domain.Meal_Plan_Snack_Domain import Meal_Plan_Snack_Domain
    from domain.Client_Domain import Client_Domain
    from domain.Dietitian_Domain import Dietitian_Domain
    from domain.Staged_Client_Domain import Staged_Client_Domain
    from domain.Order_Meal_Domain import Order_Meal_Domain
    from domain.Scheduled_Order_Meal_Domain import Scheduled_Order_Meal_Domain
    from domain.Meal_Subscription_Domain import Meal_Subscription_Domain
    from domain.Meal_Subscription_Invoice_Domain import Meal_Subscription_Invoice_Domain
    from domain.Meal_Shipment_Domain import Meal_Shipment_Domain
    from domain.Recipe_Ingredient_Domain import Recipe_Ingredient_Domain
    from domain.Order_Discount_Domain import Order_Discount_Domain
    from domain.Staged_Schedule_Meal_Domain import Staged_Schedule_Meal_Domain
    from domain.Dietitian_Prepayment_Domain import Dietitian_Prepayment_Domain
    from domain.Dietitian_Prepayment_Domain import Dietitian_Prepayment_Domain
    from domain.Prepaid_Order_Discount_Domain import Prepaid_Order_Discount_Domain
    from domain.USDA_Ingredient_Portion_Domain import USDA_Ingredient_Portion_Domain
    from domain.USDA_Ingredient_Nutrient_Domain import USDA_Ingredient_Nutrient_Domain
    from domain.Recipe_Ingredient_Nutrient_Domain import (
        Recipe_Ingredient_Nutrient_Domain,
    )
    from domain.Snack_Domain import Snack_Domain
    from domain.Order_Snack_Domain import Order_Snack_Domain
    from domain.Scheduled_Order_Snack_Domain import Scheduled_Order_Snack_Domain

    from dto.USDA_Nutrient_Mapper_DTO import USDA_Nutrient_Mapper_DTO

load_dotenv()

app: Flask = Flask(__name__)
username = os.getenv("DB_USER", GCP_Secret_Manager_Service().get_secret("DB_USER"))
password = os.getenv(
    "DB_PASSWORD", GCP_Secret_Manager_Service().get_secret("DB_PASSWORD")
)
connection_string_beginning = "postgresql://"
connection_string_end = "@localhost:5432/nourishdb"
connection_string = (
    connection_string_beginning + username + ":" + password + connection_string_end
)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DB_STRING", connection_string)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

USDA_api_key = os.getenv(
    "USDA_API_KEY", GCP_Secret_Manager_Service().get_secret("USDA_API_KEY")
)

env = os.getenv("DEPLOYMENT_ENV", "debug")


host_url = ""
if env == "debug":
    host_url = "http://localhost:3000"
    STRIPE_API_KEY = os.getenv("STRIPE_KEY")
    SHIPPO_API_KEY = os.getenv("SHIPPO_KEY")

    from flask_cors import CORS

    CORS(app)

    # --> MEALS <--

    # $12 / week
    stripe_meal_price_id = "price_1MEKY0FseFjpsgWvnbtiZYuZ"

    # $12
    stripe_one_time_meal_price_id = "price_1MEKb4FseFjpsgWvRqYXFawF"

    # $6
    stripe_one_time_fnce_discounted_meal_price_id = "price_1MEKh0FseFjpsgWvxgj4nR0T"

    # --> SNACKS <--

    # $6 / week
    stripe_snack_price_id = "price_1N1Tb4FseFjpsgWvnbpfAAIX"

    # $6
    stripe_one_time_snack_price_id = "price_1N1TfrFseFjpsgWvpuP9hhx3"

    # $3
    stripe_one_time_fnce_discounted_snack_price_id = "price_1N1Th8FseFjpsgWvzgqVuMPJ"

    # --> SHIPPING <--

    # $14 / week
    stripe_shipping_price_id = "price_1MEKYVFseFjpsgWv6vuzKoqV"

    # $14
    stripe_one_time_shipping_price_id = "price_1MEKavFseFjpsgWvWl5cWMbp"

    # $0.5
    stripe_one_time_account_setup_fee = "price_1MJ07mFseFjpsgWvsQToDJFu"

else:
    from werkzeug.middleware.proxy_fix import ProxyFix

    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)
    STRIPE_API_KEY = GCP_Secret_Manager_Service().get_secret("STRIPE_KEY")

    if env == "staging":
        host_url = "https://staging.bendito.io"
        SHIPPO_API_KEY = GCP_Secret_Manager_Service().get_secret("SHIPPO_TEST_KEY")

        # --> MEALS <--

        # $1.1 / week
        stripe_meal_price_id = "price_1MFOinFseFjpsgWvgPHNHzaq"

        # $1.1
        stripe_one_time_meal_price_id = "price_1MFOjqFseFjpsgWvyJ8eWfxw"

        # $1
        stripe_one_time_fnce_discounted_meal_price_id = "price_1LauS8FseFjpsgWvFp0xZNAU"

        # --> SNACKS <--

        # $0.6 / week
        stripe_snack_price_id = "price_1N1TrGFseFjpsgWvkL7onf2k"

        # $0.6
        stripe_one_time_snack_price_id = "price_1N1Ts4FseFjpsgWvW4heb5Oq"

        # $0.5
        stripe_one_time_fnce_discounted_snack_price_id = (
            "price_1N1TsOFseFjpsgWvWjsqserh"
        )

        # --> SHIPPING <--

        # $1.2 / week
        stripe_shipping_price_id = "price_1MFOlBFseFjpsgWvgQ8qnLZM"

        # $1.2
        stripe_one_time_shipping_price_id = "price_1MFOlHFseFjpsgWvfGZsC1Dm"

        # $0.5
        stripe_one_time_account_setup_fee = "price_1MJ06nFseFjpsgWv16WGfto4"

    elif env == "production":
        host_url = "https://bendito.io"
        SHIPPO_API_KEY = GCP_Secret_Manager_Service().get_secret("SHIPPO_KEY")

        # --> MEALS <--

        # $12 / week
        stripe_meal_price_id = "price_1MFLb4FseFjpsgWv9kHmHCMg"

        # $12
        stripe_one_time_meal_price_id = "price_1MFLd7FseFjpsgWvKZckcfMX"

        # $6
        stripe_one_time_fnce_discounted_meal_price_id = "price_1MMdGsFseFjpsgWvsJjAELxk"

        # --> SNACKS <--

        # $6 / week
        stripe_snack_price_id = "price_1N1TtmFseFjpsgWvED8ZSvW1"

        # $6
        stripe_one_time_snack_price_id = "price_1N1TtxFseFjpsgWvluWLxfxV"

        # $3
        stripe_one_time_fnce_discounted_snack_price_id = (
            "price_1N1TuBFseFjpsgWvVa2vYm1K"
        )

        # --> SHIPPING <--

        # $14 / week
        stripe_shipping_price_id = "price_1MFLbYFseFjpsgWvhkesuznl"

        # $14
        stripe_one_time_shipping_price_id = "price_1MFLcvFseFjpsgWvfPAcFUHx"

        # $0.5
        stripe_one_time_account_setup_fee = "price_1MJ06nFseFjpsgWv16WGfto4"

stripe.api_key = STRIPE_API_KEY
shippo.config.api_key = SHIPPO_API_KEY


jwt_secret = os.getenv(
    "JWT_SECRET", GCP_Secret_Manager_Service().get_secret("JWT_SECRET")
)
stripe_endpoint_secret = os.getenv(
    "STRIPE_ENDPOINT_SECRET",
    GCP_Secret_Manager_Service().get_secret("STRIPE_ENDPOINT_SECRET"),
)


# full stripe fee is .029 * total + .3 per transaction
stripe_fee_percentage = 0.029

# inclusive of stripe fees. minimum order is 60, plus .3 fixed fee, divided by 1 - .29 = 62.1. divide this by 6 to get price inclusive of stripe fee
meal_price = 12.0
snack_price = 2.0
shipping_price = 14.0

db = SQLAlchemy(app)


class Client_Model(db.Model):
    __tablename__ = "client"
    id = db.Column(db.String(80), primary_key=True, unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    dietitian_id = db.Column(
        db.String(80), db.ForeignKey("dietitian.id"), nullable=False
    )
    meal_plan_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("meal_plan.id"), nullable=False
    )
    stripe_id = db.Column(db.String(80), unique=True, nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    street = db.Column(db.String(100), nullable=False)
    suite = db.Column(db.String(80), nullable=False)
    city = db.Column(db.String(80), nullable=False)
    state = db.Column(db.String(80), nullable=False)
    zipcode = db.Column(db.String(5), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    phone_number = db.Column(db.BigInteger(), nullable=False)
    datetime = db.Column(db.Float(), nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)
    dietitian_id = db.Column(
        db.String(80), db.ForeignKey("dietitian.id"), nullable=False
    )
    notes = db.Column(db.String(500), default="")

    meal_plan = relationship("Meal_Plan_Model", lazy=True)
    meal_subscription = relationship("Meal_Subscription_Model", lazy=True)

    def __init__(self, client_domain: "Client_Domain") -> None:
        self.id = client_domain.id
        self.password = generate_password_hash(client_domain.password)
        self.dietitian_id = client_domain.dietitian_id
        self.meal_plan_id = client_domain.meal_plan_id
        self.stripe_id = client_domain.stripe_id
        self.first_name = client_domain.first_name
        self.last_name = client_domain.last_name
        self.street = client_domain.street
        self.suite = client_domain.suite
        self.city = client_domain.city
        self.state = client_domain.state
        self.zipcode = client_domain.zipcode
        self.address = client_domain.address
        self.phone_number = client_domain.phone_number
        self.datetime = client_domain.datetime
        self.active = client_domain.active

    def update(self, requested_client: "Client_Domain") -> None:
        self.password = requested_client.password
        self.dietitian_id = requested_client.dietitian_id
        self.meal_plan_id = requested_client.meal_plan_id
        self.stripe_id = requested_client.stripe_id
        self.first_name = requested_client.first_name
        self.last_name = requested_client.last_name
        self.street = requested_client.street
        self.city = requested_client.city
        self.state = requested_client.state
        self.zipcode = requested_client.zipcode
        self.address = requested_client.address
        self.phone_number = requested_client.phone_number
        self.notes = requested_client.notes
        self.datetime = requested_client.datetime
        self.active = requested_client.active


class Staged_Client_Model(db.Model):
    __tablename__ = "staged_client"
    id = db.Column(db.String(80), primary_key=True, nullable=False)
    dietitian_id = db.Column(
        db.String(80), db.ForeignKey("dietitian.id"), nullable=False
    )
    meal_plan_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("meal_plan.id"), nullable=False
    )
    first_name = db.Column(db.String(80), nullable=False)
    notes = db.Column(db.String(500), default="")
    datetime = db.Column(db.Float(), nullable=False)
    account_created = db.Column(db.Boolean(), default=True, nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)
    waitlisted = db.Column(db.Boolean(), default=False, nullable=False)
    meals_pre_selected = db.Column(db.Boolean(), default=False, nullable=False)
    meals_prepaid = db.Column(db.Boolean(), default=False, nullable=False)

    meal_plan = relationship("Meal_Plan_Model", lazy="joined")

    def __init__(self, staged_client_domain: "Staged_Client_Domain") -> None:
        self.id = staged_client_domain.id
        self.first_name = staged_client_domain.first_name
        self.dietitian_id = staged_client_domain.dietitian_id
        self.meal_plan_id = staged_client_domain.meal_plan_id
        self.notes = staged_client_domain.notes
        self.datetime = staged_client_domain.datetime
        self.account_created = staged_client_domain.account_created
        self.active = staged_client_domain.active
        self.waitlisted = staged_client_domain.waitlisted
        self.meals_pre_selected = staged_client_domain.meals_pre_selected
        self.meals_prepaid = staged_client_domain.meals_prepaid


class Dietitian_Model(db.Model):
    __tablename__ = "dietitian"
    id = db.Column(db.String(80), primary_key=True, unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    clinic_zipcode = db.Column(db.String(5), nullable=False)
    clinic_name = db.Column(db.String(80), nullable=False)

    datetime = db.Column(db.Float(), nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)

    clients = relationship("Client_Model", lazy=True)
    staged_clients = relationship("Staged_Client_Model", lazy=True)

    def __init__(self, dietitian_domain: "Dietitian_Domain") -> None:
        self.id = dietitian_domain.id
        self.password = generate_password_hash(dietitian_domain.password)
        self.first_name = dietitian_domain.first_name
        self.last_name = dietitian_domain.last_name
        self.clinic_name = dietitian_domain.clinic_name
        self.clinic_zipcode = dietitian_domain.clinic_zipcode
        self.datetime = dietitian_domain.datetime
        self.active = dietitian_domain.active


class State_Sales_Tax_Model(db.Model):
    __tablename__ = "state_sales_tax"
    state = db.Column(db.String(80), primary_key=True, unique=True, nullable=False)
    sales_tax_percentage = db.Column(db.Float(), nullable=False)
    stripe_tax_id = db.Column(db.String(80), nullable=False)

    def __init__(
        self, state: str, sales_tax_percentage: float, stripe_tax_id: str
    ) -> None:
        self.state = state
        self.sales_tax_percentage = sales_tax_percentage
        self.stripe_tax_id = stripe_tax_id


class Meal_Plan_Model(db.Model):
    __tablename__ = "meal_plan"
    id = db.Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False)
    number = db.Column(db.Integer(), unique=True, nullable=False)
    breakfast_calories = db.Column(db.Integer(), nullable=False)
    lunch_calories = db.Column(db.Integer(), nullable=False)
    dinner_calories = db.Column(db.Integer(), nullable=False)
    stated_caloric_lower_bound = db.Column(db.Integer(), nullable=False)
    stated_caloric_upper_bound = db.Column(db.Integer(), nullable=False)
    number_of_snacks = db.Column(db.Float(), nullable=False)
    per_snack_caloric_lower_bound = db.Column(db.Integer(), nullable=False)
    per_snack_caloric_upper_bound = db.Column(db.Integer(), nullable=False)

    usda_nutrient_daily_values = relationship(
        "USDA_Nutrient_Daily_Value_Model", lazy=True
    )

    def __init__(self, meal_plan_dict: dict) -> None:
        self.id = meal_plan_dict["id"]
        self.number = meal_plan_dict["number"]
        self.breakfast_calories = meal_plan_dict["breakfast_calories"]
        self.lunch_calories = meal_plan_dict["lunch_calories"]
        self.dinner_calories = meal_plan_dict["dinner_calories"]
        self.stated_caloric_lower_bound = meal_plan_dict["stated_caloric_lower_bound"]
        self.stated_caloric_upper_bound = meal_plan_dict["stated_caloric_upper_bound"]
        self.number_of_snacks = meal_plan_dict["number_of_snacks"]
        self.per_snack_caloric_lower_bound = meal_plan_dict[
            "per_snack_caloric_lower_bound"
        ]
        self.per_snack_caloric_upper_bound = meal_plan_dict[
            "per_snack_caloric_upper_bound"
        ]
        self.active = meal_plan_dict["active"]


class Meal_Model(db.Model):
    __tablename__ = "meal"
    id = db.Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False)
    meal_time = db.Column(db.String(80), nullable=False)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float(), nullable=False)
    image_url = db.Column(db.String(200), nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)

    dietary_restrictions = relationship("Meal_Dietary_Restriction_Model", lazy=True)

    def __init__(self, meal_domain: "Meal_Domain") -> None:
        self.id = meal_domain.id
        self.meal_time = meal_domain.meal_time
        self.name = meal_domain.name
        self.description = meal_domain.description
        self.price = meal_domain.price
        self.image_url = meal_domain.image_url
        self.active = meal_domain.active

    @property
    def lower_case_name(self) -> str:
        return self.name.lower()


class Meal_Plan_Meal_Model(db.Model):
    __tablename__ = "meal_plan_meal"
    id = db.Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False)
    meal_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("meal.id"), primary_key=True, nullable=False
    )
    meal_plan_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("meal_plan.id"),
        primary_key=True,
        nullable=False,
    )
    active = db.Column(db.Boolean(), default=True, nullable=False)
    recipe = relationship("Recipe_Ingredient_Model", lazy="joined")
    associated_meal = relationship("Meal_Model", lazy="joined")
    associated_meal_plan = relationship("Meal_Plan_Model", lazy="joined")

    def __init__(self, meal_plan_meal_domain: "Meal_Plan_Meal_Domain") -> None:
        self.id = meal_plan_meal_domain.id
        self.meal_id = meal_plan_meal_domain.meal_id
        self.meal_plan_id = meal_plan_meal_domain.meal_plan_id
        self.active = meal_plan_meal_domain.active

    def update(self, meal_plan_meal: "Meal_Plan_Meal_Domain") -> None:
        self.k_cal = meal_plan_meal.k_cal
        self.protein_k_cal = meal_plan_meal.protein_k_cal
        self.carb_k_cal = meal_plan_meal.carb_k_cal
        self.fat_k_cal = meal_plan_meal.fat_k_cal


class Order_Meal_Model(db.Model):
    __tablename__ = "order_meal"
    id = db.Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False)
    meal_subscription_invoice_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("meal_subscription_invoice.id"),
        nullable=False,
    )
    scheduled_order_meal_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("scheduled_order_meal.id"), nullable=True
    )
    # Relationships
    scheduled_order_meal = relationship("Scheduled_Order_Meal_Model", lazy="joined")

    def __init__(self, order_meal: "Order_Meal_Domain") -> None:
        self.id = order_meal.id
        self.meal_subscription_invoice_id = order_meal.meal_subscription_invoice_id
        self.scheduled_order_meal_id = order_meal.scheduled_order_meal_id


class Snack_Model(db.Model):
    __tablename__ = "snack"
    id = db.Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float(), nullable=False)
    image_url = db.Column(db.String(200), nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)

    def __init__(self, snack_domain: "Snack_Domain") -> None:
        self.id = snack_domain.id
        self.name = snack_domain.name
        self.description = snack_domain.description
        self.price = snack_domain.price
        self.image_url = snack_domain.image_url
        self.active = snack_domain.active

    @property
    def lower_case_name(self) -> str:
        return self.name.lower()


class Meal_Plan_Snack_Model(db.Model):
    __tablename__ = "meal_plan_snack"
    id = db.Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False)
    snack_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("snack.id"), primary_key=True, nullable=False
    )
    meal_plan_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("meal_plan.id"),
        primary_key=True,
        nullable=False,
    )
    active = db.Column(db.Boolean(), default=True, nullable=False)
    recipe = relationship("Recipe_Ingredient_Model", lazy="joined")
    associated_snack = relationship("Snack_Model", lazy="joined")
    associated_meal_plan = relationship("Meal_Plan_Model", lazy="joined")

    def __init__(self, meal_plan_snack_domain: "Meal_Plan_Snack_Domain") -> None:
        self.id = meal_plan_snack_domain.id
        self.snack_id = meal_plan_snack_domain.snack_id
        self.meal_plan_id = meal_plan_snack_domain.meal_plan_id
        self.active = meal_plan_snack_domain.active

    def update(self, meal_plan_meal: "Meal_Plan_Snack_Domain") -> None:
        self.k_cal = meal_plan_meal.k_cal
        self.protein_k_cal = meal_plan_meal.protein_k_cal
        self.carb_k_cal = meal_plan_meal.carb_k_cal
        self.fat_k_cal = meal_plan_meal.fat_k_cal


class Order_Snack_Model(db.Model):
    __tablename__ = "order_snack"
    id = db.Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False)
    meal_subscription_invoice_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("meal_subscription_invoice.id"),
        nullable=False,
    )
    scheduled_order_snack_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("scheduled_order_snack.id"), nullable=True
    )
    # Relationships
    scheduled_order_snack = relationship("Scheduled_Order_Snack_Model", lazy="joined")

    def __init__(self, order_snack: "Order_Snack_Domain") -> None:
        self.id = order_snack.id
        self.meal_subscription_invoice_id = order_snack.meal_subscription_invoice_id
        self.scheduled_order_snack_id = order_snack.scheduled_order_snack_id


class Meal_Shipment_Model(db.Model):
    __tablename__ = "meal_shipment"

    id = db.Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False)
    meal_subscription_invoice_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("meal_subscription_invoice.id"),
        nullable=False,
    )
    shippo_transaction_id = db.Column(db.String(200), nullable=False)
    label_url = db.Column(db.String(200), nullable=False)
    tracking_number = db.Column(db.String(200), nullable=False)
    tracking_url = db.Column(db.String(200), nullable=False)

    def __init__(self, meal_shipment: "Meal_Shipment_Domain") -> None:
        self.id = meal_shipment.id
        self.meal_subscription_invoice_id = meal_shipment.meal_subscription_invoice_id
        self.shippo_transaction_id = meal_shipment.shippo_transaction_id
        self.label_url = meal_shipment.label_url
        self.tracking_number = meal_shipment.tracking_number
        self.tracking_url = meal_shipment.tracking_url


class Meal_Subscription_Invoice_Model(db.Model):
    __tablename__ = "meal_subscription_invoice"

    id = db.Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False)
    meal_subscription_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("meal_subscription.id"), nullable=False
    )
    subtotal = db.Column(db.Float(), nullable=False)
    sales_tax_percentage = db.Column(db.Float(), nullable=False)
    sales_tax_total = db.Column(db.Float(), nullable=False)
    shipping_total = db.Column(db.Float(), nullable=False)
    stripe_fee_total = db.Column(db.Float(), nullable=False)
    stripe_invoice_id = db.Column(db.String(200), nullable=False)
    stripe_payment_intent_id = db.Column(db.String(200), nullable=False)
    total = db.Column(db.Float(), nullable=False)
    datetime = db.Column(db.Float(), nullable=False)
    delivery_date = db.Column(db.Float(), nullable=False)

    def __init__(
        self, meal_subscription_invoice_domain: "Meal_Subscription_Invoice_Domain"
    ) -> None:
        self.id = meal_subscription_invoice_domain.id
        self.meal_subscription_id = (
            meal_subscription_invoice_domain.meal_subscription_id
        )
        self.subtotal = meal_subscription_invoice_domain.subtotal
        self.sales_tax_percentage = (
            meal_subscription_invoice_domain.sales_tax_percentage
        )
        self.sales_tax_total = meal_subscription_invoice_domain.sales_tax_total
        self.shipping_total = meal_subscription_invoice_domain.shipping_total
        self.stripe_fee_total = meal_subscription_invoice_domain.stripe_fee_total
        self.stripe_invoice_id = meal_subscription_invoice_domain.stripe_invoice_id
        self.stripe_payment_intent_id = (
            meal_subscription_invoice_domain.stripe_payment_intent_id
        )
        self.total = meal_subscription_invoice_domain.total
        self.datetime = meal_subscription_invoice_domain.datetime
        self.delivery_date = meal_subscription_invoice_domain.delivery_date

    order_meals: Mapped[list[Order_Meal_Model]] = relationship(
        "Order_Meal_Model", lazy=True
    )
    order_snacks: Mapped[list[Order_Snack_Model]] = relationship(
        "Order_Snack_Model", lazy=True
    )
    meal_shipments: Mapped[list[Meal_Shipment_Model]] = relationship(
        "Meal_Shipment_Model", lazy=True
    )


class Scheduled_Order_Meal_Model(db.Model):
    __tablename__ = "scheduled_order_meal"
    id = db.Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False)
    meal_subscription_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("meal_subscription.id"), nullable=False
    )
    meal_id = db.Column(UUID(as_uuid=True), db.ForeignKey("meal.id"), nullable=False)
    delivery_date = db.Column(db.Float(), nullable=False)
    delivery_skipped = db.Column(db.Boolean(), default=False, nullable=False)
    delivery_paused = db.Column(db.Boolean(), default=False, nullable=False)
    datetime = db.Column(db.Float(), nullable=False)

    associated_meal = relationship("Meal_Model", lazy="joined")

    def __init__(
        self, scheduled_order_meal_domain: "Scheduled_Order_Meal_Domain"
    ) -> None:
        self.id = scheduled_order_meal_domain.id
        self.meal_subscription_id = scheduled_order_meal_domain.meal_subscription_id
        self.meal_id = scheduled_order_meal_domain.meal_id
        self.delivery_date = scheduled_order_meal_domain.delivery_date
        self.delivery_skipped = scheduled_order_meal_domain.delivery_skipped
        self.delivery_paused = scheduled_order_meal_domain.delivery_paused
        self.datetime = scheduled_order_meal_domain.datetime


class Schedule_Meal_Model(db.Model):
    __tablename__ = "schedule_meal"
    id = db.Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False)
    meal_id = db.Column(UUID(as_uuid=True), db.ForeignKey("meal.id"), nullable=False)
    meal_subscription_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("meal_subscription.id"), nullable=False
    )
    associated_meal = relationship("Meal_Model", lazy="joined")


class Staged_Schedule_Meal_Model(db.Model):
    __tablename__ = "staged_schedule_meal"
    id = db.Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False)
    meal_id = db.Column(UUID(as_uuid=True), db.ForeignKey("meal.id"), nullable=False)
    staged_client_id = db.Column(
        db.String(80), db.ForeignKey("staged_client.id"), nullable=False
    )
    dietitian_prepayment_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("dietitian_prepayment.id"), nullable=True
    )

    associated_meal = relationship("Meal_Model", lazy="joined")

    def __init__(
        self, staged_schedule_meal_domain: "Staged_Schedule_Meal_Domain"
    ) -> None:
        self.id = staged_schedule_meal_domain.id
        self.meal_id = staged_schedule_meal_domain.meal_id
        self.staged_client_id = staged_schedule_meal_domain.staged_client_id


class Scheduled_Order_Snack_Model(db.Model):
    __tablename__ = "scheduled_order_snack"
    id = db.Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False)
    meal_subscription_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("meal_subscription.id"), nullable=False
    )
    snack_id = db.Column(UUID(as_uuid=True), db.ForeignKey("snack.id"), nullable=False)
    delivery_date = db.Column(db.Float(), nullable=False)
    delivery_skipped = db.Column(db.Boolean(), default=False, nullable=False)
    delivery_paused = db.Column(db.Boolean(), default=False, nullable=False)
    datetime = db.Column(db.Float(), nullable=False)

    associated_snack = relationship("Snack_Model", lazy="joined")

    def __init__(
        self, scheduled_order_snack_domain: "Scheduled_Order_Snack_Domain"
    ) -> None:
        self.id = scheduled_order_snack_domain.id
        self.meal_subscription_id = scheduled_order_snack_domain.meal_subscription_id
        self.snack_id = scheduled_order_snack_domain.snack_id
        self.delivery_date = scheduled_order_snack_domain.delivery_date
        self.delivery_skipped = scheduled_order_snack_domain.delivery_skipped
        self.delivery_paused = scheduled_order_snack_domain.delivery_paused
        self.datetime = scheduled_order_snack_domain.datetime


class Schedule_Snack_Model(db.Model):
    __tablename__ = "schedule_snack"
    id = db.Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False)
    snack_id = db.Column(UUID(as_uuid=True), db.ForeignKey("snack.id"), nullable=False)
    meal_subscription_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("meal_subscription.id"), nullable=False
    )
    associated_snack = relationship("Snack_Model", lazy="joined")


class Meal_Subscription_Model(db.Model):
    __tablename__ = "meal_subscription"
    id = db.Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False)
    client_id = db.Column(db.String(80), db.ForeignKey("client.id"), nullable=False)
    dietitian_id = db.Column(
        db.String(80), db.ForeignKey("dietitian.id"), nullable=False
    )
    stripe_subscription_id = db.Column(db.String(80), unique=True, nullable=False)
    stripe_price_id = db.Column(db.String(80), nullable=False)
    datetime = db.Column(db.Float(), nullable=False)
    shipping_cost = db.Column(db.Float(), nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)
    paused = db.Column(db.Boolean(), default=False, nullable=False)

    def __init__(self, meal_subscription: "Meal_Subscription_Domain") -> None:
        self.id = meal_subscription.id
        self.client_id = meal_subscription.client_id
        self.dietitian_id = meal_subscription.dietitian_id
        self.stripe_subscription_id = meal_subscription.stripe_subscription_id
        self.stripe_price_id = meal_subscription.stripe_price_id
        self.datetime = meal_subscription.datetime
        self.shipping_cost = meal_subscription.shipping_cost
        self.active = meal_subscription.active
        self.paused = meal_subscription.paused


class Meal_Dietary_Restriction_Model(db.Model):
    __tablename__ = "meal_dietary_restriction"
    id = db.Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False)
    dietary_restriction_id = db.Column(
        db.String(80), db.ForeignKey("dietary_restriction.id"), nullable=False
    )
    meal_id = db.Column(UUID(as_uuid=True), db.ForeignKey("meal.id"), nullable=False)

    def __init__(
        self, meal_dietary_restriction_domain: "Meal_Dietary_Restriction_Domain"
    ) -> None:
        self.id = meal_dietary_restriction_domain.id
        self.dietary_restriction_id = (
            meal_dietary_restriction_domain.dietary_restriction_id
        )
        self.meal_id = meal_dietary_restriction_domain.meal_id


class Dietary_Restriction_Model(db.Model):
    __tablename__ = "dietary_restriction"
    id = db.Column(db.String(80), primary_key=True, unique=True, nullable=False)

    meal_dietary_restriction: Mapped[
        list[Meal_Dietary_Restriction_Model]
    ] = relationship("Meal_Dietary_Restriction_Model", lazy=True)


class USDA_Ingredient_Model(db.Model):
    __tablename__ = "usda_ingredient"

    id = db.Column(db.String(80), primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(80), unique=True, nullable=False)
    fdc_id = db.Column(db.String(80), unique=True, nullable=False)
    fda_identifier = db.Column(db.String(80), unique=True, nullable=False)
    amount_of_grams = db.Column(db.Float(), nullable=False)
    k_cal = db.Column(db.Integer(), nullable=False)
    k_cal_to_gram_ratio = db.Column(db.Float(), nullable=False)
    usda_data_type = db.Column(db.String(80), nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)

    portions = relationship("USDA_Ingredient_Portion_Model", lazy="joined")

    def __init__(
        self, usda_ingredient_nutrient_mapper: "USDA_Nutrient_Mapper_DTO"
    ) -> None:
        self.id = usda_ingredient_nutrient_mapper.usda_ingredient_id
        self.name = usda_ingredient_nutrient_mapper.usda_ingredient_name
        self.fdc_id = usda_ingredient_nutrient_mapper.fdc_id
        self.fda_identifier = usda_ingredient_nutrient_mapper.fda_identifier
        self.amount_of_grams = usda_ingredient_nutrient_mapper.amount_of_grams
        self.k_cal = usda_ingredient_nutrient_mapper.calories
        self.k_cal_to_gram_ratio = (
            usda_ingredient_nutrient_mapper.calories_to_grams_ratio
        )
        self.usda_data_type = usda_ingredient_nutrient_mapper.usda_data_type
        self.active = True

    def update(self, updated_recipe_ingredient: "Recipe_Ingredient_Domain") -> None:
        self.id = updated_recipe_ingredient.usda_ingredient_id


class Recipe_Ingredient_Model(db.Model):
    __tablename__ = "recipe_ingredient"
    __table_args__ = (
        CheckConstraint(
            "NOT(meal_plan_meal_id IS NULL AND meal_plan_snack_id IS NULL)"
        ),
    )
    id = db.Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False)
    usda_ingredient_id = db.Column(
        db.String(80),
        db.ForeignKey("usda_ingredient.id"),
        primary_key=True,
        nullable=False,
    )
    meal_plan_meal_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("meal_plan_meal.id"),
        nullable=True,
    )
    meal_plan_snack_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("meal_plan_snack.id"),
        nullable=True,
    )
    usda_ingredient_portion_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("usda_ingredient_portion.id"), nullable=False
    )
    quantity = db.Column(db.Float(), nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)
    usda_ingredient_portion = relationship(
        "USDA_Ingredient_Portion_Model", lazy="joined"
    )
    nutrients: Mapped[list["Recipe_Ingredient_Nutrient_Model"]] = relationship(
        "Recipe_Ingredient_Nutrient_Model", lazy="joined"
    )
    usda_ingredient = relationship("USDA_Ingredient_Model", lazy=True)

    def __init__(self, recipe_ingredient_domain: "Recipe_Ingredient_Domain") -> None:
        self.id = recipe_ingredient_domain.id
        self.usda_ingredient_id = recipe_ingredient_domain.usda_ingredient_id
        self.meal_plan_meal_id = recipe_ingredient_domain.meal_plan_meal_id
        self.meal_plan_snack_id = recipe_ingredient_domain.meal_plan_snack_id
        self.usda_ingredient_portion_id = (
            recipe_ingredient_domain.usda_ingredient_portion_id
        )
        self.quantity = recipe_ingredient_domain.quantity
        self.active = recipe_ingredient_domain.active


class USDA_Ingredient_Portion_Model(db.Model):
    __tablename__ = "usda_ingredient_portion"
    id = db.Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False)
    usda_ingredient_id = db.Column(
        db.String(80), db.ForeignKey("usda_ingredient.id"), nullable=False
    )
    fda_portion_id = db.Column(db.String(80), nullable=False)
    non_metric_unit = db.Column(db.String(80), nullable=False)
    grams_per_non_metric_unit = db.Column(db.Float(), nullable=False)
    portion_description = db.Column(db.String(80), nullable=False)
    is_imperial = db.Column(db.Boolean(), default=True, nullable=False)
    usda_data_type = db.Column(db.String(80), nullable=False)
    custom_value = db.Column(db.Boolean(), default=False, nullable=False)

    def __init__(
        self, usda_ingredient_portion_domain: "USDA_Ingredient_Portion_Domain"
    ) -> None:
        self.id = usda_ingredient_portion_domain.id
        self.usda_ingredient_id = usda_ingredient_portion_domain.usda_ingredient_id
        self.fda_portion_id = usda_ingredient_portion_domain.fda_portion_id
        self.non_metric_unit = usda_ingredient_portion_domain.non_metric_unit
        self.grams_per_non_metric_unit = (
            usda_ingredient_portion_domain.grams_per_non_metric_unit
        )
        self.portion_description = usda_ingredient_portion_domain.portion_description
        self.is_imperial = usda_ingredient_portion_domain.is_imperial
        self.usda_data_type = usda_ingredient_portion_domain.usda_data_type


class Imperial_Unit_Model(db.Model):
    __tablename__ = "imperial_unit"
    id = db.Column(db.String(80), primary_key=True, unique=True, nullable=False)

    ounces = db.Column(db.Float(), nullable=False)


class Nutrient_Model(db.Model):
    __tablename__ = "nutrient"
    id = db.Column(db.String(80), primary_key=True, unique=True, nullable=False)
    unit = db.Column(db.String(80), nullable=False)
    name = db.Column(db.String(80), primary_key=True, unique=True, nullable=False)
    usda_id = db.Column(db.String(80), unique=True, nullable=False)
    has_daily_value = db.Column(db.Boolean(), default=True, nullable=False)

    def __init__(self, nutrient_dict: dict) -> None:
        self.id = nutrient_dict["id"]
        self.unit = nutrient_dict["unit"]
        self.name = nutrient_dict["name"]
        if nutrient_dict["usda_id"] == "N/A":
            self.usda_id = ""
        else:
            self.usda_id = nutrient_dict["usda_id"]
        self.has_daily_value = nutrient_dict["has_daily_value"]


class USDA_Ingredient_Nutrient_Model(db.Model):
    __tablename__ = "usda_ingredient_nutrient"
    id = db.Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False)
    usda_ingredient_id = db.Column(
        db.String(80), db.ForeignKey("usda_ingredient.id"), nullable=False
    )
    nutrient_id = db.Column(db.String(80), db.ForeignKey("nutrient.id"), nullable=False)
    amount = db.Column(db.Float(), nullable=False)

    def __init__(
        self, usda_ingredient_nutrient_domain: "USDA_Ingredient_Nutrient_Domain" = None
    ) -> None:
        if usda_ingredient_nutrient_domain:
            self.id = usda_ingredient_nutrient_domain.id
            self.usda_ingredient_id = usda_ingredient_nutrient_domain.usda_ingredient_id
            self.nutrient_id = usda_ingredient_nutrient_domain.nutrient_id
            self.amount = usda_ingredient_nutrient_domain.amount


class Recipe_Ingredient_Nutrient_Model(db.Model):
    __tablename__ = "recipe_ingredient_nutrient"
    id = db.Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False)
    recipe_ingredient_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("recipe_ingredient.id"), nullable=False
    )
    nutrient_id = db.Column(db.String(80), db.ForeignKey("nutrient.id"), nullable=False)
    usda_nutrient_daily_value_amount = db.Column(db.Float(), nullable=False)
    amount = db.Column(db.Float(), nullable=False)

    nutrient: Mapped[Nutrient_Model] = relationship("Nutrient_Model", lazy="joined")

    def __init__(
        self, recipe_ingredient_nutrient_domain: "Recipe_Ingredient_Nutrient_Domain"
    ) -> None:
        self.id = recipe_ingredient_nutrient_domain.id
        self.recipe_ingredient_id = (
            recipe_ingredient_nutrient_domain.recipe_ingredient_id
        )
        self.nutrient_id = recipe_ingredient_nutrient_domain.nutrient_id
        self.usda_nutrient_daily_value_amount = (
            recipe_ingredient_nutrient_domain.usda_nutrient_daily_value_amount
        )
        self.amount = recipe_ingredient_nutrient_domain.amount


class USDA_Nutrient_Daily_Value_Model(db.Model):
    __tablename__ = "usda_nutrient_daily_value"
    id = db.Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False)
    nutrient_id = db.Column(
        db.String(80), db.ForeignKey("nutrient.id"), primary_key=True, nullable=False
    )
    meal_plan_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("meal_plan.id"),
        primary_key=True,
        nullable=False,
    )
    amount = db.Column(db.Float(), nullable=False)
    unit = db.Column(db.String(80), nullable=False)

    def __init__(self, usda_nutrient_daily_value_dict: dict) -> None:
        self.id = usda_nutrient_daily_value_dict["id"]
        self.nutrient_id = usda_nutrient_daily_value_dict["nutrient_id"]
        self.meal_plan_id = usda_nutrient_daily_value_dict["meal_plan_id"]
        self.amount = usda_nutrient_daily_value_dict["amount"]
        self.unit = usda_nutrient_daily_value_dict["unit"]


class Email_Tracker_Model(db.Model):
    __tablename__ = "settings"
    date_email_sent = db.Column(
        db.Date(), primary_key=True, unique=True, nullable=False
    )


class FNCE_Lead_Model(db.Model):
    __tablename__ = "fnce_lead"
    id = db.Column(db.String(80), primary_key=True, unique=True, nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    is_dietitian = db.Column(db.Boolean(), nullable=False)
    is_student = db.Column(db.Boolean(), nullable=False)
    description = db.Column(db.String(300), nullable=False)

    def __init__(self, fnce_lead_dict: dict) -> None:
        self.id = fnce_lead_dict["id"]
        self.first_name = fnce_lead_dict["first_name"]
        self.last_name = fnce_lead_dict["last_name"]
        self.is_dietitian = fnce_lead_dict["is_dietitian"]
        self.is_student = fnce_lead_dict["is_student"]
        self.description = fnce_lead_dict["description"]


class Discount_Model(db.Model):
    __tablename__ = "discount"
    id = db.Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False)
    code = db.Column(db.String(20), unique=True, nullable=False)
    discount_percentage = db.Column(db.Float(), nullable=False)
    active = db.Column(db.Boolean(), nullable=False)

    def __init__(self, discount_dict: dict) -> None:
        self.id = discount_dict["id"]
        self.code = discount_dict["code"]
        self.discount_percentage = discount_dict["discount_percentage"]
        self.active = discount_dict["active"]


class Prepaid_Order_Discount_Model(db.Model):
    __tablename__ = "prepaid_order_discount"
    discount_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("discount.id"),
        primary_key=True,
        nullable=False,
    )
    dietitian_prepayment_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("dietitian_prepayment.id"),
        primary_key=True,
        nullable=False,
    )
    amount = db.Column(db.Float(), nullable=False)
    datetime = db.Column(db.Float(), nullable=False)

    def __init__(
        self, prepaid_order_discount_domain: "Prepaid_Order_Discount_Domain"
    ) -> None:
        self.discount_id = prepaid_order_discount_domain.discount_id
        self.dietitian_prepayment_id = (
            prepaid_order_discount_domain.dietitian_prepayment_id
        )
        self.amount = prepaid_order_discount_domain.amount
        self.datetime = prepaid_order_discount_domain.datetime


class Order_Discount_Model(db.Model):
    __tablename__ = "order_discount"
    discount_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("discount.id"),
        primary_key=True,
        nullable=False,
    )
    staged_client_id = db.Column(
        db.String(80),
        db.ForeignKey("staged_client.id"),
        primary_key=True,
        nullable=False,
    )
    amount = db.Column(db.Float(), nullable=False)
    datetime = db.Column(db.Float(), nullable=False)

    def __init__(self, order_discount_domain: "Order_Discount_Domain") -> None:
        self.discount_id = order_discount_domain.discount_id
        self.staged_client_id = order_discount_domain.staged_client_id
        self.amount = order_discount_domain.amount
        self.datetime = order_discount_domain.datetime


class Dietitian_Prepayment_Model(db.Model):
    __tablename__ = "dietitian_prepayment"
    id = db.Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False)
    dietitian_id = db.Column(
        db.String(80), db.ForeignKey("dietitian.id"), primary_key=True, nullable=False
    )
    staged_client_id = db.Column(
        db.String(80),
        db.ForeignKey("staged_client.id"),
        primary_key=True,
        nullable=False,
    )
    subtotal = db.Column(db.Float(), nullable=False)
    sales_tax_percentage = db.Column(db.Float(), nullable=False)
    sales_tax_total = db.Column(db.Float(), nullable=False)
    shipping_total = db.Column(db.Float(), nullable=False)
    stripe_fee_total = db.Column(db.Float(), nullable=False)
    stripe_payment_intent_id = db.Column(db.String(200), nullable=False)
    total = db.Column(db.Float(), nullable=False)
    datetime = db.Column(db.Float(), nullable=False)

    def __init__(
        self, dietitian_prepayment_domain: "Dietitian_Prepayment_Domain"
    ) -> None:
        self.id = dietitian_prepayment_domain.id
        self.dietitian_id = dietitian_prepayment_domain.dietitian_id
        self.staged_client_id = dietitian_prepayment_domain.staged_client_id
        self.subtotal = dietitian_prepayment_domain.subtotal
        self.sales_tax_percentage = dietitian_prepayment_domain.sales_tax_percentage
        self.sales_tax_total = dietitian_prepayment_domain.sales_tax_total
        self.shipping_total = dietitian_prepayment_domain.shipping_total
        self.stripe_fee_total = dietitian_prepayment_domain.stripe_fee_total
        self.shipping_total = dietitian_prepayment_domain.shipping_total
        self.stripe_payment_intent_id = (
            dietitian_prepayment_domain.stripe_payment_intent_id
        )
        self.total = dietitian_prepayment_domain.total
        self.datetime = dietitian_prepayment_domain.datetime


@compiles(DropTable, "postgresql")
def _compile_drop_table(element, compiler, **kwargs):
    return compiler.visit_drop_table(element) + " CASCADE"


def load_json(filename) -> dict:
    with open(filename) as file:
        jsn = json.load(file)
        file.close()
        return jsn


def create_dietary_restrictions() -> None:
    dietary_restrictions = ["vegetarian"]
    for dietary_restriction in dietary_restrictions:
        new_dietary_restriction = Dietary_Restriction_Model(id=dietary_restriction)
        db.session.add(new_dietary_restriction)
    db.session.commit()


def create_state_tax_rates() -> None:
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


def create_imperial_units() -> None:
    imperial_units = [
        {"name": "teaspoon", "ounces": 0.166667},
        {"name": "tablespoon", "ounces": 0.5},
        {"ounces": 8.0, "name": "cup"},
        {"name": "oz", "ounces": 1.0},
    ]
    for unit in imperial_units:
        new_imperial_unit = Imperial_Unit_Model(id=unit["name"], ounces=unit["ounces"])
        db.session.add(new_imperial_unit)
    db.session.commit()


def create_new_meal_plans() -> None:
    meal_plans = load_json("nutrient_data/new_meal_plans.json")
    for meal_plan in meal_plans:
        new_meal_plan = Meal_Plan_Model(meal_plan_dict=meal_plan)
        db.session.add(new_meal_plan)
    db.session.commit()


def create_new_meals() -> None:
    meals = load_json("nutrient_data/new_meals.json")
    for meal in meals:
        new_meal = Meal_Model(meal_dict=meal)
        for meal_dietary_restriction in meal["dietary_restrictions"]:
            new_meal_dietary_restriction = Meal_Dietary_Restriction_Model(
                meal_dietary_restriction_dict=meal_dietary_restriction
            )
            db.session.add(new_meal_dietary_restriction)
        db.session.add(new_meal)
    db.session.commit()


def create_new_usda_ingredients() -> None:
    usda_ingredients = load_json("nutrient_data/new_usda_ingredients.json")
    for usda_ingredient in usda_ingredients:
        new_usda_ingredient = USDA_Ingredient_Model(
            usda_ingredient_dict=usda_ingredient
        )
        db.session.add(new_usda_ingredient)
    db.session.commit()


def create_new_nutrients() -> None:
    nutrients = load_json("nutrient_data/new_nutrients.json")
    for nutrient in nutrients:
        new_nutrient = Nutrient_Model(nutrient_dict=nutrient)
        db.session.add(new_nutrient)
    db.session.commit()


def create_new_usda_ingredient_nutrients() -> None:
    usda_ingredient_nutrients = load_json(
        "nutrient_data/new_usda_ingredient_nutrients.json"
    )
    for usda_ingredient_nutrient in usda_ingredient_nutrients:
        if (
            usda_ingredient_nutrient["nutrient_id"] != "net_carb"
            and usda_ingredient_nutrient["nutrient_id"] != "pantothenic_acid"
            and usda_ingredient_nutrient["nutrient_id"] != "biotin"
        ):
            new_usda_ingredient_nutrient = USDA_Ingredient_Nutrient_Model(
                usda_ingredient_nutrient_dict=usda_ingredient_nutrient
            )
        db.session.add(new_usda_ingredient_nutrient)
    db.session.commit()


def create_usda_ingredient_data() -> None:
    from service.USDA_API_Service import USDA_API_Service
    from domain.Imperial_Unit_Domain import Imperial_Unit_Domain
    from domain.Nutrient_Domain import Nutrient_Domain
    from dto.USDA_Nutrient_Mapper_DTO import USDA_Nutrient_Mapper_DTO

    usda_ingredients = load_json("nutrient_data/new_usda_ingredients.json")
    imperial_units = [
        Imperial_Unit_Domain(imperial_unit_object=x)
        for x in db.session.query(Imperial_Unit_Model).all()
    ]
    nutrients = [
        Nutrient_Domain(nutrient_object=x)
        for x in db.session.query(Nutrient_Model).all()
    ]
    for usda_ingredient in usda_ingredients:
        fdc_id = usda_ingredient["fdc_id"]
        print("fdc_id b4 fetch", fdc_id)
        usda_ingredient_id = usda_ingredient["id"]
        usda_ingredient_name = usda_ingredient["name"]
        usda_ingredient_data = USDA_API_Service(
            USDA_api_key=USDA_api_key
        ).get_ingredient(fdc_id=fdc_id)
        print("after fetch")
        mapped_usda_ingredient_data = USDA_Nutrient_Mapper_DTO(
            usda_ingredient_id=usda_ingredient_id,
            usda_ingredient_name=usda_ingredient_name,
            fdc_id=fdc_id,
            usda_ingredient_data=usda_ingredient_data,
            nutrients_list=nutrients,
            imperial_units=imperial_units,
        )
        print("after map")
        new_usda_ingredient = USDA_Ingredient_Model(
            usda_ingredient_nutrient_mapper=mapped_usda_ingredient_data
        )
        db.session.add(new_usda_ingredient)

        for nutrient in mapped_usda_ingredient_data.nutrients:
            new_usda_ingredient_nutrient = USDA_Ingredient_Nutrient_Model(
                usda_ingredient_nutrient_domain=nutrient
            )
            db.session.add(new_usda_ingredient_nutrient)

        for portion in mapped_usda_ingredient_data.portions:
            new_usda_ingredient_portion = USDA_Ingredient_Portion_Model(
                usda_ingredient_portion_domain=portion
            )
            db.session.add(new_usda_ingredient_portion)
        print("after add everything")
    db.session.commit()


def create_new_usda_ingredient_portions() -> None:
    new_usda_ingredient_portions = load_json(
        "nutrient_data/new_usda_ingredient_portions.json"
    )
    for usda_ingrient_portion in new_usda_ingredient_portions:
        new_usda_ingredient_portion = USDA_Ingredient_Portion_Model(
            usda_ingredient_portion_dict=usda_ingrient_portion
        )
        db.session.add(new_usda_ingredient_portion)
    db.session.commit()


def create_new_meal_plan_meals() -> None:
    meal_plan_meals = load_json("nutrient_data/new_meal_plan_meals.json")
    for meal_plan_meal in meal_plan_meals:
        new_meal_plan_meal = Meal_Plan_Meal_Model(meal_plan_meal_dict=meal_plan_meal)
        db.session.add(new_meal_plan_meal)
    db.session.commit()


def create_new_recipe_ingredients() -> None:
    recipe_ingredients = load_json("nutrient_data/new_recipe_ingredients.json")
    for recipe_ingredient in recipe_ingredients:
        new_recipe_ingredient = Recipe_Ingredient_Model(
            recipe_ingredient_dict=recipe_ingredient
        )
        db.session.add(new_recipe_ingredient)
    db.session.commit()


def create_new_usda_nutrient_daily_values() -> None:
    daily_nutrient_values = load_json(
        "nutrient_data/new_usda_nutrient_daily_values.json"
    )
    for daily_nutrient_value in daily_nutrient_values:
        daily_nutrient_value["id"] = uuid.uuid4()
        new_daily_value = USDA_Nutrient_Daily_Value_Model(
            usda_nutrient_daily_value_dict=daily_nutrient_value
        )
        db.session.add(new_daily_value)
    db.session.commit()


def create_new_recipe_ingredient_nutrients() -> None:
    recipe_ingredient_nutrients = load_json(
        "nutrient_data/new_recipe_ingredient_nutrients.json"
    )
    for recipe_ingredient_nutrient in recipe_ingredient_nutrients:
        if (
            recipe_ingredient_nutrient["nutrient_id"] != "net_carb"
            and recipe_ingredient_nutrient["nutrient_id"] != "pantothenic_acid"
            and recipe_ingredient_nutrient["nutrient_id"] != "biotin"
        ):
            new_recipe_ingredient_nutrient = Recipe_Ingredient_Nutrient_Model(
                recipe_ingredient_nutrient_dict=recipe_ingredient_nutrient
            )
        db.session.add(new_recipe_ingredient_nutrient)
    db.session.commit()


def create_discount() -> None:
    new_discount_dict = {
        "id": uuid.uuid4(),
        "code": "FNCE 2022",
        "discount_percentage": 0.5,
        "active": True,
    }
    new_discount = Discount_Model(discount_dict=new_discount_dict)
    db.session.add(new_discount)
    db.session.commit()


# TODO write tests for create USDA_Nutrient_Mapper_DTO,
# Then populate the database with the new data,
# Then create ExtendedUSDAIngredientDomain and associated services to return data to MenuBuilder
# Then iterate on MenuBuilder to create new meals, meal plan meals, and recipe ingredients


def new_gcp_models_initialization() -> None:
    db.drop_all()
    print("Dropped all tables")
    db.create_all()
    print("Created all tables")
    create_imperial_units()
    print("Created imperial units")
    create_new_meal_plans()
    print("Created new meal plans")
    create_dietary_restrictions()
    print("Created dietary restrictions")
    create_state_tax_rates()
    print("Created state tax rates")
    create_discount()
    print("Created discount")
    create_new_nutrients()
    print("Created new nutrients")
    create_usda_ingredient_data()
    print("Created usda ingredient data")

    # Might update this function later
    create_new_usda_nutrient_daily_values()
    print("Created new usda nutrient daily values")
    # Meals, Meal Plan Meals, and Recipe Ingredients are created in the MenuBuilder


def new_instantiate_db_connection() -> None:
    from pathlib import Path

    cwd = os.getcwd()
    if cwd.endswith("bendito-api"):
        server_path = Path(".").joinpath("flask-server")
        os.chdir(server_path)
    new_gcp_models_initialization()


def wipe_all_meal_related_data() -> None:
    meals = db.session.query(Meal_Model).all()
    meal_plan_meals = db.session.query(Meal_Plan_Meal_Model).all()
    for meal_plan_meal in meal_plan_meals:
        for recipe_ingredient in meal_plan_meal.recipe:
            for recipe_ingredient_nutrient in recipe_ingredient.nutrients:
                db.session.delete(recipe_ingredient_nutrient)
            db.session.delete(recipe_ingredient)
        db.session.delete(meal_plan_meal)
    for meal in meals:
        for meal_dietary_restriction in meal.dietary_restrictions:
            db.session.delete(meal_dietary_restriction)
        db.session.delete(meal)
    db.session.commit()


def wipe_all_snack_related_data() -> None:
    snacks = db.session.query(Snack_Model).all()
    meal_plan_snacks = db.session.query(Meal_Plan_Snack_Model).all()
    for meal_plan_snack in meal_plan_snacks:
        for recipe_ingredient in meal_plan_snack.recipe:
            for recipe_ingredient_nutrient in recipe_ingredient.nutrients:
                db.session.delete(recipe_ingredient_nutrient)
            db.session.delete(recipe_ingredient)
        db.session.delete(meal_plan_snack)
    for snack in snacks:
        db.session.delete(snack)
    db.session.commit()


def wipe_meal_data(meal_id: UUID) -> None:
    meal = db.session.query(Meal_Model).filter(Meal_Model.id == meal_id).first()
    if meal:
        meal_plan_meals = (
            db.session.query(Meal_Plan_Meal_Model)
            .filter(Meal_Plan_Meal_Model.meal_id == meal_id)
            .all()
        )
        for meal_plan_meal in meal_plan_meals:
            for recipe_ingredient in meal_plan_meal.recipe:
                for recipe_ingredient_nutrient in recipe_ingredient.nutrients:
                    db.session.delete(recipe_ingredient_nutrient)
                db.session.delete(recipe_ingredient)
            db.session.delete(meal_plan_meal)
        for meal_dietary_restriction in meal.dietary_restrictions:
            db.session.delete(meal_dietary_restriction)
        db.session.delete(meal)
        db.session.commit()


def wipe_snack_data(snack_id: UUID) -> None:
    snack = db.session.query(Snack_Model).filter(Snack_Model.id == snack_id).first()
    if snack:
        snack_plan_snacks = (
            db.session.query(Meal_Plan_Snack_Model)
            .filter(Meal_Plan_Snack_Model.snack_id == snack_id)
            .all()
        )
        for snack_plan_snack in snack_plan_snacks:
            for recipe_ingredient in snack_plan_snack.recipe:
                for recipe_ingredient_nutrient in recipe_ingredient.nutrients:
                    db.session.delete(recipe_ingredient_nutrient)
                db.session.delete(recipe_ingredient)
            db.session.delete(snack_plan_snack)


def wipe_all_usda_ingredient_related_data(usda_ingredient_id: str) -> None:
    usda_ingredient = (
        db.session.query(USDA_Ingredient_Model)
        .filter(USDA_Ingredient_Model.id == usda_ingredient_id)
        .first()
    )
    nutrients = (
        db.session.query(USDA_Ingredient_Nutrient_Model)
        .filter(USDA_Ingredient_Nutrient_Model.usda_ingredient_id == usda_ingredient.id)
        .all()
    )
    for usda_ingredient_nutrient in nutrients:
        db.session.delete(usda_ingredient_nutrient)
    for usda_ingredient_portion in usda_ingredient.portions:
        db.session.delete(usda_ingredient_portion)
    db.session.commit()
    db.session.delete(usda_ingredient)
    db.session.commit()
