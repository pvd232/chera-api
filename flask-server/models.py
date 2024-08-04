from service.GCP_Secret_Manager_Service import GCP_Secret_Manager_Service
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy.dialects.postgresql import UUID
import os
from sqlalchemy.schema import DropTable, CheckConstraint
from sqlalchemy.ext.compiler import compiles
import stripe
import shippo
from typing import TYPE_CHECKING
from helpers.db.get_db_connection_string import get_db_connection_string
from authlib.integrations.flask_client import OAuth

if TYPE_CHECKING:
    from domain.Meal_Sample_Shipment_Domain import Meal_Sample_Shipment_Domain
    from domain.Meal_Sample_Domain import Meal_Sample_Domain
    from domain.COGS_Domain import COGS_Domain
    from domain.Eating_Disorder_Domain import Eating_Disorder_Domain
    from domain.Dietary_Restriction_Domain import Dietary_Restriction_Domain
    from domain.USDA_Ingredient_Domain import USDA_Ingredient_Domain
    from domain.Meal_Plan_Domain import Meal_Plan_Domain
    from domain.Discount_Domain import Discount_Domain
    from domain.USDA_Nutrient_Daily_Value_Domain import USDA_Nutrient_Daily_Value_Domain
    from domain.Nutrient_Domain import Nutrient_Domain
    from domain.Imperial_Unit_Domain import Imperial_Unit_Domain
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
    from domain.Staged_Schedule_Snack_Domain import Staged_Schedule_Snack_Domain
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

app = Flask(__name__)


username = os.getenv("DB_USER") or GCP_Secret_Manager_Service().get_secret("DB_USER")
password = os.getenv("DB_PASSWORD") or GCP_Secret_Manager_Service().get_secret(
    "DB_PASSWORD"
)
print("username", username)
print("password", password)
connection_string = os.getenv("DB_STRING") or get_db_connection_string(
    username=username, password=password, db_name="chera-prod-db"
)
print("connection_string", connection_string)

app.config["SQLALCHEMY_DATABASE_URI"] = connection_string
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

USDA_api_key = os.getenv("USDA_API_KEY") or GCP_Secret_Manager_Service().get_secret(
    "USDA_API_KEY"
)

# Env var from cloud run
env = os.getenv("DEPLOYMENT_ENV") or "debug"
print("env", env)

################### Auth0 ###################
oauth = OAuth(app)
app.secret_key = os.getenv("APP_SECRET_KEY") or GCP_Secret_Manager_Service().get_secret(
    "APP_SECRET_KEY"
)
oauth.register(
    "auth0",
    client_id=os.getenv("AUTH0_CLIENT_ID"),
    client_secret=os.getenv("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{os.getenv("AUTH0_DOMAIN")}/.well-known/openid-configuration',
)
#############################################

host_url = ""
if env == "debug":
    host_url = "http://localhost:3000"
    STRIPE_API_KEY = os.getenv("STRIPE_KEY")
    SHIPPO_API_KEY = os.getenv("SHIPPO_KEY")

    from flask_cors import CORS

    CORS(app)

    # $0.5
    stripe_one_time_account_setup_fee = "price_1MJ07mFseFjpsgWvsQToDJFu"

else:
    STRIPE_API_KEY = GCP_Secret_Manager_Service().get_secret("STRIPE_KEY")
    # $0.5
    stripe_one_time_account_setup_fee = "price_1NO5JyFseFjpsgWvp0VOYr3a"

    if env == "staging":
        host_url = "https://staging.cherahealth.com"
        SHIPPO_API_KEY = GCP_Secret_Manager_Service().get_secret("SHIPPO_TEST_KEY")

    elif env == "production":
        host_url = "https://cherahealth.com"
        SHIPPO_API_KEY = GCP_Secret_Manager_Service().get_secret("SHIPPO_KEY")

stripe.api_key = STRIPE_API_KEY
shippo.config.api_key = SHIPPO_API_KEY

jwt_secret = os.getenv("JWT_SECRET") or GCP_Secret_Manager_Service().get_secret(
    "JWT_SECRET"
)

stripe_invoice_endpoint_secret = os.getenv(
    "STRIPE_INVOICE_ENDPOINT_SECRET"
) or GCP_Secret_Manager_Service().get_secret("STRIPE_INVOICE_ENDPOINT_SECRET")

# full stripe fee is .029 * total + .3 per transaction
stripe_fee_percentage = 0.029


db = SQLAlchemy(app)


class Client_Model(db.Model):
    __tablename__ = "client"
    id = db.Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False)
    email = db.Column(db.String(40), nullable=False)
    dietitian_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("dietitian.id"),
        nullable=True,
    )
    meal_plan_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("meal_plan.id"), nullable=False
    )
    stripe_id = db.Column(db.String(80), unique=True, nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    street = db.Column(db.String(100), nullable=False)
    suite = db.Column(db.String(20), nullable=False)
    city = db.Column(db.String(40), nullable=False)
    state = db.Column(db.String(13), nullable=False)
    zipcode = db.Column(db.String(5), nullable=False)
    zipcode_extension = db.Column(db.String(4), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    datetime = db.Column(db.Float(), nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)
    notes = db.Column(db.String(500), default="")

    meal_plan = relationship("Meal_Plan_Model", lazy=True)
    meal_subscription = relationship("Meal_Subscription_Model", lazy=True)

    def __init__(self, client_domain: "Client_Domain") -> None:
        self.id = client_domain.id
        self.email = client_domain.email
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
        self.zipcode_extension = client_domain.zipcode_extension
        self.address = client_domain.address
        self.phone_number = client_domain.phone_number
        self.datetime = client_domain.datetime
        self.active = client_domain.active

    def update(self, client_domain: "Client_Domain") -> None:
        self.dietitian_id = client_domain.dietitian_id
        self.meal_plan_id = client_domain.meal_plan_id
        self.stripe_id = client_domain.stripe_id
        self.first_name = client_domain.first_name
        self.last_name = client_domain.last_name
        self.street = client_domain.street
        self.city = client_domain.city
        self.state = client_domain.state
        self.zipcode = client_domain.zipcode
        self.zipcode_extension = client_domain.zipcode_extension
        self.address = client_domain.address
        self.phone_number = client_domain.phone_number
        self.notes = client_domain.notes
        self.datetime = client_domain.datetime
        self.active = client_domain.active

    def update_address(self, client_domain: "Client_Domain") -> None:
        self.suite = client_domain.suite
        self.street = client_domain.street
        self.city = client_domain.city
        self.state = client_domain.state
        self.zipcode = client_domain.zipcode
        self.zipcode_extension = client_domain.zipcode_extension
        self.address = client_domain.address


class Eating_Disorder_Model(db.Model):
    __tablename__ = "eating_disorder"
    id = db.Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(80), nullable=False)

    def __init__(self, eating_disorder_domain: "Eating_Disorder_Domain") -> None:
        self.id = eating_disorder_domain.id
        self.name = eating_disorder_domain.name


class COGS_Model(db.Model):
    __tablename__ = "cogs"
    num_meals = db.Column(db.Integer(), primary_key=True, nullable=False)
    is_local = db.Column(db.Boolean(), primary_key=True, nullable=False)
    ingredient = db.Column(db.Float(), nullable=False)
    core_packaging = db.Column(db.Float(), nullable=False)
    kitchen = db.Column(db.Float(), nullable=False)
    chef = db.Column(db.Float(), nullable=False)
    box = db.Column(db.Float(), nullable=False)
    ice = db.Column(db.Float(), nullable=False)
    num_boxes = db.Column(db.Integer(), nullable=False)

    def __init__(self, cogs_domain: "COGS_Domain") -> None:
        self.num_meals = cogs_domain.num_meals
        self.is_local = cogs_domain.is_local
        self.ingredient = cogs_domain.ingredient
        self.core_packaging = cogs_domain.core_packaging
        self.kitchen = cogs_domain.kitchen
        self.chef = cogs_domain.chef
        self.box = cogs_domain.box
        self.ice = cogs_domain.ice
        self.num_boxes = cogs_domain.num_boxes


class Staged_Client_Model(db.Model):
    __tablename__ = "staged_client"
    id = db.Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False)
    email = db.Column(db.String(40), nullable=False)
    dietitian_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("dietitian.id", ondelete="CASCADE"),
        nullable=True,
    )
    meal_plan_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("meal_plan.id"), nullable=False
    )
    eating_disorder_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("eating_disorder.id"), nullable=False
    )
    # personal information
    first_name = db.Column(db.String(80), nullable=False)
    current_weight = db.Column(db.Integer(), nullable=False)
    target_weight = db.Column(db.Integer(), nullable=False)
    age = db.Column(db.Integer(), nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    notes = db.Column(db.String(500), default="")
    # account information
    datetime = db.Column(db.Float(), nullable=False)
    account_created = db.Column(db.Boolean(), default=True, nullable=False)
    waitlisted = db.Column(db.Boolean(), default=False, nullable=False)
    meals_pre_selected = db.Column(db.Boolean(), default=False, nullable=False)
    meals_prepaid = db.Column(db.Boolean(), default=False, nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)

    # relationships
    meal_plan = relationship("Meal_Plan_Model", lazy="joined")
    eating_disorder = relationship("Eating_Disorder_Model", lazy="joined")

    def __init__(self, staged_client_domain: "Staged_Client_Domain") -> None:
        self.id = staged_client_domain.id
        self.email = staged_client_domain.email
        # personal information
        self.first_name = staged_client_domain.first_name
        self.current_weight = staged_client_domain.current_weight
        self.target_weight = staged_client_domain.target_weight
        self.age = staged_client_domain.age
        self.gender = staged_client_domain.gender
        self.notes = staged_client_domain.notes
        self.eating_disorder_id = staged_client_domain.eating_disorder_id
        # Account information
        self.dietitian_id = staged_client_domain.dietitian_id
        self.meal_plan_id = staged_client_domain.meal_plan_id
        self.datetime = staged_client_domain.datetime
        self.account_created = staged_client_domain.account_created
        self.active = staged_client_domain.active
        self.waitlisted = staged_client_domain.waitlisted
        self.meals_pre_selected = staged_client_domain.meals_pre_selected
        self.meals_prepaid = staged_client_domain.meals_prepaid


class Dietitian_Model(db.Model):
    __tablename__ = "dietitian"
    id = db.Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False)
    email = db.Column(db.String(40), nullable=False)
    phone_number = db.Column(db.String(20), default="", nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    dietetic_registration_number = db.Column(db.String(20), nullable=False)
    clinic_city = db.Column(db.String(40), nullable=False)
    clinic_state = db.Column(db.String(2), nullable=False)
    clinic_address = db.Column(db.String(200), nullable=False)
    number_of_ed_clients = db.Column(db.Integer(), nullable=False)
    datetime = db.Column(db.Float(), nullable=False)
    got_sample = db.Column(db.Boolean(), default=False, nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)

    clients = relationship("Client_Model", lazy=True, passive_deletes=True)
    staged_clients = relationship(
        "Staged_Client_Model", lazy=True, passive_deletes=True
    )
    meal_samples = relationship("Meal_Sample_Model", lazy=True, passive_deletes=True)
    meal_sample_shipments = relationship(
        "Meal_Sample_Shipment_Model", lazy=True, passive_deletes=True
    )

    def __init__(self, dietitian_domain: "Dietitian_Domain") -> None:
        self.id = dietitian_domain.id
        self.email = dietitian_domain.email
        self.phone_number = dietitian_domain.phone_number
        self.first_name = dietitian_domain.first_name
        self.last_name = dietitian_domain.last_name
        self.dietetic_registration_number = (
            dietitian_domain.dietetic_registration_number
        )
        self.clinic_city = dietitian_domain.clinic_city
        self.clinic_state = dietitian_domain.clinic_state
        self.clinic_address = dietitian_domain.clinic_address
        self.number_of_ed_clients = dietitian_domain.number_of_ed_clients
        self.datetime = dietitian_domain.datetime
        self.got_sample = dietitian_domain.got_sample
        self.active = dietitian_domain.active


class State_Sales_Tax_Model(db.Model):
    __tablename__ = "state_sales_tax"
    state = db.Column(db.String(13), primary_key=True, unique=True, nullable=False)
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

    def __init__(
        self, meal_plan_dict: dict = None, meal_plan_domain: "Meal_Plan_Domain" = None
    ) -> None:
        if meal_plan_dict:
            self.id = meal_plan_dict["id"]
            self.number = meal_plan_dict["number"]
            self.breakfast_calories = meal_plan_dict["breakfast_calories"]
            self.lunch_calories = meal_plan_dict["lunch_calories"]
            self.dinner_calories = meal_plan_dict["dinner_calories"]
            self.stated_caloric_lower_bound = meal_plan_dict[
                "stated_caloric_lower_bound"
            ]
            self.stated_caloric_upper_bound = meal_plan_dict[
                "stated_caloric_upper_bound"
            ]
            self.number_of_snacks = meal_plan_dict["number_of_snacks"]
            self.per_snack_caloric_lower_bound = meal_plan_dict[
                "per_snack_caloric_lower_bound"
            ]
            self.per_snack_caloric_upper_bound = meal_plan_dict[
                "per_snack_caloric_upper_bound"
            ]
            self.active = meal_plan_dict["active"]
        elif meal_plan_domain:
            self.id = meal_plan_domain.id
            self.number = meal_plan_domain.number
            self.breakfast_calories = meal_plan_domain.breakfast_calories
            self.lunch_calories = meal_plan_domain.lunch_calories
            self.dinner_calories = meal_plan_domain.dinner_calories
            self.stated_caloric_lower_bound = (
                meal_plan_domain.stated_caloric_lower_bound
            )
            self.stated_caloric_upper_bound = (
                meal_plan_domain.stated_caloric_upper_bound
            )
            self.number_of_snacks = meal_plan_domain.number_of_snacks
            self.per_snack_caloric_lower_bound = (
                meal_plan_domain.per_snack_caloric_lower_bound
            )
            self.per_snack_caloric_upper_bound = (
                meal_plan_domain.per_snack_caloric_upper_bound
            )


class Meal_Model(db.Model):
    __tablename__ = "meal"
    id = db.Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False)
    meal_time = db.Column(db.String(15), nullable=False)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(200), nullable=False)
    image_url = db.Column(db.String(200), nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)

    dietary_restrictions = relationship("Meal_Dietary_Restriction_Model", lazy=True)

    def __init__(self, meal_domain: "Meal_Domain") -> None:
        self.id = meal_domain.id
        self.meal_time = meal_domain.meal_time
        self.name = meal_domain.name
        self.description = meal_domain.description
        self.image_url = meal_domain.image_url
        self.active = meal_domain.active


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
    multiplier = db.Column(db.Float(), default=1.0, nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)
    recipe = relationship("Recipe_Ingredient_Model", lazy="joined")
    associated_meal = relationship("Meal_Model", lazy="joined")
    associated_meal_plan = relationship("Meal_Plan_Model", lazy="joined")

    def __init__(self, meal_plan_meal_domain: "Meal_Plan_Meal_Domain") -> None:
        self.id: UUID = meal_plan_meal_domain.id
        self.meal_id: UUID = meal_plan_meal_domain.meal_id
        self.meal_plan_id: UUID = meal_plan_meal_domain.meal_plan_id
        self.multiplier: float = meal_plan_meal_domain.multiplier
        self.active: bool = meal_plan_meal_domain.active

    def update_multiplier(self, meal_plan_meal: "Meal_Plan_Meal_Domain") -> None:
        self.multiplier = meal_plan_meal.multiplier


class Order_Meal_Model(db.Model):
    __tablename__ = "order_meal"
    id = db.Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False)
    meal_subscription_invoice_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("meal_subscription_invoice.id"),
        nullable=False,
    )
    scheduled_order_meal_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("scheduled_order_meal.id"), nullable=False
    )
    # Relationships
    scheduled_order_meal = relationship("Scheduled_Order_Meal_Model", lazy="joined")

    def __init__(self, order_meal: "Order_Meal_Domain") -> None:
        self.id = order_meal.id
        self.meal_subscription_invoice_id = order_meal.meal_subscription_invoice_id
        self.scheduled_order_meal_id = order_meal.scheduled_order_meal_id


class Meal_Sample_Model(db.Model):
    __tablename__ = "meal_sample"
    id = db.Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False)
    meal_id = db.Column(UUID(as_uuid=True), db.ForeignKey("meal.id"), nullable=False)
    dietitian_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("dietitian.id", ondelete="CASCADE"),
        nullable=False,
    )

    def __init__(self, meal_sample_domain: "Meal_Sample_Domain") -> None:
        self.id = meal_sample_domain.id
        self.meal_id = meal_sample_domain.meal_id
        self.dietitian_id = meal_sample_domain.dietitian_id


class Snack_Model(db.Model):
    __tablename__ = "snack"
    id = db.Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(200), nullable=False)
    image_url = db.Column(db.String(200), nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)

    def __init__(self, snack_domain: "Snack_Domain") -> None:
        self.id = snack_domain.id
        self.name = snack_domain.name
        self.description = snack_domain.description
        self.image_url = snack_domain.image_url
        self.active = snack_domain.active


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
    multiplier = db.Column(db.Float(), default=1.0, nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)
    recipe = relationship("Recipe_Ingredient_Model", lazy="joined")
    associated_snack = relationship("Snack_Model", lazy="joined")
    associated_meal_plan = relationship("Meal_Plan_Model", lazy="joined")

    def __init__(self, meal_plan_snack_domain: "Meal_Plan_Snack_Domain") -> None:
        self.id = meal_plan_snack_domain.id
        self.snack_id = meal_plan_snack_domain.snack_id
        self.meal_plan_id = meal_plan_snack_domain.meal_plan_id
        self.multiplier = meal_plan_snack_domain.multiplier
        self.active = meal_plan_snack_domain.active

    def update_multiplier(self, meal_plan_snack: "Meal_Plan_Snack_Domain") -> None:
        self.multiplier = meal_plan_snack.multiplier


class Order_Snack_Model(db.Model):
    __tablename__ = "order_snack"
    id = db.Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False)
    meal_subscription_invoice_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("meal_subscription_invoice.id"),
        nullable=False,
    )
    scheduled_order_snack_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("scheduled_order_snack.id"), nullable=False
    )
    # Relationships
    scheduled_order_snack = relationship("Scheduled_Order_Snack_Model", lazy="joined")

    def __init__(self, order_snack: "Order_Snack_Domain") -> None:
        self.id = order_snack.id
        self.meal_subscription_invoice_id = order_snack.meal_subscription_invoice_id
        self.scheduled_order_snack_id = order_snack.scheduled_order_snack_id


class Meal_Sample_Shipment_Model(db.Model):
    __tablename__ = "meal_sample_shipment"

    id = db.Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False)
    dietitian_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("dietitian.id", ondelete="CASCADE"),
        nullable=False,
    )
    shippo_transaction_id = db.Column(db.String(80), nullable=False)
    label_url = db.Column(db.String(200), nullable=False)
    tracking_number = db.Column(db.String(80), nullable=False)
    tracking_url = db.Column(db.String(200), nullable=False)

    def __init__(
        self, meal_sample_shipment_domain: "Meal_Sample_Shipment_Domain"
    ) -> None:
        self.id = meal_sample_shipment_domain.id
        self.dietitian_id = meal_sample_shipment_domain.dietitian_id
        self.shippo_transaction_id = meal_sample_shipment_domain.shippo_transaction_id
        self.label_url = meal_sample_shipment_domain.label_url
        self.tracking_number = meal_sample_shipment_domain.tracking_number
        self.tracking_url = meal_sample_shipment_domain.tracking_url


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
    stripe_invoice_id = db.Column(db.String(100), nullable=False)
    stripe_payment_intent_id = db.Column(db.String(100), nullable=False)
    total = db.Column(db.Float(), nullable=False)
    datetime = db.Column(db.Float(), nullable=False)
    delivery_date = db.Column(db.Float(), nullable=False)
    payment_successful = db.Column(db.Boolean(), default=True, nullable=False)

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
        self.payment_successful = True

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
        UUID(as_uuid=True), db.ForeignKey("staged_client.id"), nullable=False
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


class Staged_Schedule_Snack_Model(db.Model):
    __tablename__ = "staged_schedule_snack"
    id = db.Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False)
    snack_id = db.Column(UUID(as_uuid=True), db.ForeignKey("snack.id"), nullable=False)
    staged_client_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("staged_client.id"), nullable=False
    )
    dietitian_prepayment_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("dietitian_prepayment.id"), nullable=True
    )

    associated_snack = relationship("Snack_Model", lazy="joined")

    def __init__(
        self, staged_schedule_snack_domain: "Staged_Schedule_Snack_Domain"
    ) -> None:
        self.id = staged_schedule_snack_domain.id
        self.snack_id = staged_schedule_snack_domain.snack_id
        self.staged_client_id = staged_schedule_snack_domain.staged_client_id


class Meal_Subscription_Model(db.Model):
    __tablename__ = "meal_subscription"
    id = db.Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False)
    client_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("client.id"), nullable=False
    )
    dietitian_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("dietitian.id"), nullable=True
    )
    stripe_subscription_id = db.Column(db.String(80), unique=True, nullable=False)
    shipping_rate = db.Column(db.Float(), nullable=False)
    datetime = db.Column(db.Float(), nullable=False)

    paused = db.Column(db.Boolean(), default=False, nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)

    def __init__(self, meal_subscription: "Meal_Subscription_Domain") -> None:
        self.id = meal_subscription.id
        self.client_id = meal_subscription.client_id
        self.dietitian_id = meal_subscription.dietitian_id
        self.stripe_subscription_id = meal_subscription.stripe_subscription_id
        self.shipping_rate = meal_subscription.shipping_rate
        self.datetime = meal_subscription.datetime

        self.active = meal_subscription.active
        self.paused = meal_subscription.paused

    def update(self, meal_subscription_domain: "Meal_Subscription_Domain") -> None:
        self.dietitian_id = meal_subscription_domain.dietitian_id
        self.stripe_subscription_id = meal_subscription_domain.stripe_subscription_id
        self.datetime = meal_subscription_domain.datetime
        self.shipping_rate = meal_subscription_domain.shipping_rate
        self.active = meal_subscription_domain.active
        self.paused = meal_subscription_domain.paused


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

    meal_dietary_restriction: Mapped[list[Meal_Dietary_Restriction_Model]] = (
        relationship("Meal_Dietary_Restriction_Model", lazy=True)
    )

    def __init__(
        self, dietary_restriction_domain: "Dietary_Restriction_Domain"
    ) -> None:
        self.id = dietary_restriction_domain.id


class USDA_Ingredient_Model(db.Model):
    __tablename__ = "usda_ingredient"

    id = db.Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(80), unique=True, nullable=False)
    fdc_id = db.Column(db.String(80), unique=True, nullable=False)
    fda_identifier = db.Column(db.String(80), unique=True, nullable=False)
    amount_of_grams = db.Column(db.Float(), nullable=False)
    k_cal = db.Column(db.Integer(), nullable=False)
    k_cal_to_gram_ratio = db.Column(db.Float(), nullable=False)
    usda_data_type = db.Column(db.String(20), nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)

    portions = relationship("USDA_Ingredient_Portion_Model", lazy="joined")

    def __init__(
        self,
        usda_ingredient_nutrient_mapper: "USDA_Nutrient_Mapper_DTO" = None,
        usda_ingredient_domain: "USDA_Ingredient_Domain" = None,
    ) -> None:
        if usda_ingredient_nutrient_mapper:
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
        elif usda_ingredient_domain:
            self.id = usda_ingredient_domain.id
            self.name = usda_ingredient_domain.name
            self.fdc_id = usda_ingredient_domain.fdc_id
            self.fda_identifier = usda_ingredient_domain.fda_identifier
            self.amount_of_grams = usda_ingredient_domain.amount_of_grams
            self.k_cal = usda_ingredient_domain.k_cal
            self.k_cal_to_gram_ratio = usda_ingredient_domain.k_cal_to_gram_ratio
            self.usda_data_type = usda_ingredient_domain.usda_data_type
            self.active = usda_ingredient_domain.active

    def update(
        self, usda_ingredient_nutrient_mapper: "USDA_Nutrient_Mapper_DTO"
    ) -> None:
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


class Recipe_Ingredient_Model(db.Model):
    __tablename__ = "recipe_ingredient"
    __table_args__ = (
        CheckConstraint(
            "NOT(meal_plan_meal_id IS NULL AND meal_plan_snack_id IS NULL)"
        ),
    )
    id = db.Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False)
    usda_ingredient_id = db.Column(
        UUID(as_uuid=True),
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
        UUID(as_uuid=True), db.ForeignKey("usda_ingredient.id"), nullable=False
    )
    fda_portion_id = db.Column(db.String(80), nullable=False)
    non_metric_unit = db.Column(db.String(80), nullable=False)
    grams_per_non_metric_unit = db.Column(db.Float(), nullable=False)
    portion_description = db.Column(db.String(80), nullable=False)
    is_imperial = db.Column(db.Boolean(), default=True, nullable=False)
    usda_data_type = db.Column(db.String(20), nullable=False)
    custom_value = db.Column(db.Boolean(), default=False, nullable=False)
    multiplier = db.Column(db.Float(), default=1, nullable=False)

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
        self.custom_value = usda_ingredient_portion_domain.custom_value
        self.multiplier = usda_ingredient_portion_domain.multiplier


class Imperial_Unit_Model(db.Model):
    __tablename__ = "imperial_unit"
    id = db.Column(db.String(80), primary_key=True, unique=True, nullable=False)

    ounces = db.Column(db.Float(), nullable=False)

    def __init__(self, imperial_unit_domain: "Imperial_Unit_Domain") -> None:
        self.id = imperial_unit_domain.id
        self.ounces = imperial_unit_domain.ounces


class Nutrient_Model(db.Model):
    __tablename__ = "nutrient"
    id = db.Column(db.String(30), primary_key=True, unique=True, nullable=False)
    unit = db.Column(db.String(10), nullable=False)
    name = db.Column(db.String(30), primary_key=True, unique=True, nullable=False)
    usda_id = db.Column(db.String(20), unique=True, nullable=False)
    has_daily_value = db.Column(db.Boolean(), default=True, nullable=False)

    def __init__(
        self, nutrient_dict: dict = None, nutrient_domain: "Nutrient_Domain" = None
    ) -> None:
        if nutrient_dict:
            self.id = nutrient_dict["id"]
            self.unit = nutrient_dict["unit"]
            self.name = nutrient_dict["name"]
            if nutrient_dict["usda_id"] == "N/A":
                self.usda_id = ""
            else:
                self.usda_id = nutrient_dict["usda_id"]
            self.has_daily_value = nutrient_dict["has_daily_value"]
        elif nutrient_domain:
            self.id = nutrient_domain.id
            self.unit = nutrient_domain.unit
            self.name = nutrient_domain.name
            self.usda_id = nutrient_domain.usda_id
            self.has_daily_value = nutrient_domain.has_daily_value


class USDA_Ingredient_Nutrient_Model(db.Model):
    __tablename__ = "usda_ingredient_nutrient"
    id = db.Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False)
    usda_ingredient_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("usda_ingredient.id"), nullable=False
    )
    nutrient_id = db.Column(db.String(30), db.ForeignKey("nutrient.id"), nullable=False)
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
    nutrient_id = db.Column(db.String(30), db.ForeignKey("nutrient.id"), nullable=False)
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
        db.String(30), db.ForeignKey("nutrient.id"), primary_key=True, nullable=False
    )
    meal_plan_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("meal_plan.id"),
        primary_key=True,
        nullable=False,
    )
    amount = db.Column(db.Float(), nullable=False)
    unit = db.Column(db.String(80), nullable=False)

    def __init__(
        self,
        usda_nutrient_daily_value_dict: dict = None,
        usda_nutrient_daily_value_domain: "USDA_Nutrient_Daily_Value_Domain" = None,
    ) -> None:
        if usda_nutrient_daily_value_dict:
            self.id = usda_nutrient_daily_value_dict["id"]
            self.nutrient_id = usda_nutrient_daily_value_dict["nutrient_id"]
            self.meal_plan_id = usda_nutrient_daily_value_dict["meal_plan_id"]
            self.amount = usda_nutrient_daily_value_dict["amount"]
            self.unit = usda_nutrient_daily_value_dict["unit"]
        elif usda_nutrient_daily_value_domain:
            self.id = usda_nutrient_daily_value_domain.id
            self.nutrient_id = usda_nutrient_daily_value_domain.nutrient_id
            self.meal_plan_id = usda_nutrient_daily_value_domain.meal_plan_id
            self.amount = usda_nutrient_daily_value_domain.amount
            self.unit = usda_nutrient_daily_value_domain.unit


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

    def __init__(
        self, discount_dict: dict = None, discount_domain: "Discount_Domain" = None
    ) -> None:
        if discount_dict:
            self.id = discount_dict["id"]
            self.code = discount_dict["code"]
            self.discount_percentage = discount_dict["discount_percentage"]
            self.active = discount_dict["active"]
        else:
            self.id = discount_domain.id
            self.code = discount_domain.code
            self.discount_percentage = discount_domain.discount_percentage
            self.active = discount_domain.active


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
        UUID(as_uuid=True),
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
        UUID(as_uuid=True),
        db.ForeignKey("dietitian.id"),
        primary_key=True,
        nullable=False,
    )
    staged_client_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("staged_client.id"),
        primary_key=True,
        nullable=False,
    )
    subtotal = db.Column(db.Float(), nullable=False)
    sales_tax_percentage = db.Column(db.Float(), nullable=False)
    sales_tax_total = db.Column(db.Float(), nullable=False)
    shipping_total = db.Column(db.Float(), nullable=False)
    stripe_fee_total = db.Column(db.Float(), nullable=False)
    stripe_payment_intent_id = db.Column(db.String(100), nullable=False)
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


class NYSAND_Lead(db.Model):
    __tablename__ = "nysand_lead"
    id = db.Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False)
    dietitian_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("dietitian.id"),
        primary_key=True,
        nullable=False,
    )

    def __init__(self, id: UUID, dietitian_id: str):
        self.id = id
        self.dietitian_id = dietitian_id


# Allows for db.drop_all() to work by setting universal cascade
@compiles(DropTable, "postgresql")
def _compile_drop_table(element, compiler, **kwargs):
    return compiler.visit_drop_table(element) + " CASCADE"
