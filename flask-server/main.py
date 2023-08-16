from uuid import UUID
import os
from models import app, db, env, host_url, oauth
from datetime import datetime, timezone
from flask import (
    Response,
    request,
    jsonify,
    url_for,
    session,
    redirect,
)
import json
from werkzeug.exceptions import HTTPException
from typing import Optional
import stripe
import uuid


@app.errorhandler(404)
def not_found(e) -> str:
    print("requested url:", request.path, "\n", "error:", e)
    return Response(status=404)


@app.errorhandler(500)
def handle_exception(e) -> HTTPException | Response:
    print()
    print("500 error exception", e)
    print()
    if isinstance(e, HTTPException):
        return e

    res = {
        "code": 500,
        "errorType": "Internal Server Error",
        "errorMessage": "Something went really wrong!",
    }
    if env == "debug":
        res["errorMessage"] = e.message if hasattr(e, "message") else f"{e}"
    return Response(status=500, response=json.dumps(res))


from helpers.Auth_Error import Auth_Error


@app.errorhandler(Auth_Error)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response


@app.route("/api/client_sign_up/<string:staged_client_id>")
def client_signup(staged_client_id: str):
    if env == "debug":
        the_scheme = "http"

    else:
        the_scheme = "https"
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True, _scheme=the_scheme),
        audience=os.getenv("AUTH0_AUDIENCE"),
        screen_hint="signup",
        response_type="code",
        state=staged_client_id,
    )


@app.route("/api/callback", methods=["GET", "POST"])
def callback():
    staged_client_id = request.args.get("state")
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    redirect_signup_url = (
        f"{host_url}/client-sign-up?staged_client_id={staged_client_id}"
    )
    return redirect(redirect_signup_url)


@app.route("/api/update_table")
def update_table() -> Response:
    from models import connection_string
    from helpers.db.update_table import update_table
    from helpers.check_auth import check_auth
    from service.GCP_Secret_Manager_Service import GCP_Secret_Manager_Service

    db_password = os.getenv("DB_PASSWORD") or GCP_Secret_Manager_Service().get_secret(
        "DB_PASSWORD"
    )

    if not check_auth(env=env, db_password=db_password, request=request):
        return Response(status=401)

    update_table(database_url=connection_string, query=request.args.get("query"))
    db.metadata.create_all(db.engine)
    return Response(status=204)


@app.route("/api/drop_table")
def drop_table() -> Response:
    from models import connection_string
    from helpers.db.drop_table import drop_table
    from helpers.check_auth import check_auth
    from service.GCP_Secret_Manager_Service import GCP_Secret_Manager_Service

    db_password = os.getenv("DB_PASSWORD") or GCP_Secret_Manager_Service().get_secret(
        "DB_PASSWORD"
    )

    if not check_auth(env=env, db_password=db_password, request=request):
        return Response(status=401)

    drop_table(database_url=connection_string, table_name="Imperial_Unit")
    db.metadata.create_all(db.engine)
    return Response(status=204)


@app.route("/api/create_tables")
def create_table() -> Response:
    from models import db
    from helpers.check_auth import check_auth
    from service.GCP_Secret_Manager_Service import GCP_Secret_Manager_Service

    db_password = os.getenv("DB_PASSWORD") or GCP_Secret_Manager_Service().get_secret(
        "DB_PASSWORD"
    )

    if not check_auth(env=env, db_password=db_password, request=request):
        return Response(status=401)

    db.metadata.create_all(db.engine)
    return Response(status=204)


@app.route("/api/setup_tables")
def setup_table() -> Response:
    from helpers.check_auth import check_auth
    from service.GCP_Secret_Manager_Service import GCP_Secret_Manager_Service

    db_password = os.getenv("DB_PASSWORD") or GCP_Secret_Manager_Service().get_secret(
        "DB_PASSWORD"
    )

    if not check_auth(env=env, db_password=db_password, request=request):
        return Response(status=401)

    db.metadata.create_all(db.engine)
    return Response(status=200)


@app.route("/api/continuity/write")
def continuity_write() -> Response:
    from repository.Discount_Repository import Discount_Repository
    from repository.Nutrient_Repository import Nutrient_Repository
    from repository.USDA_Ingredient_Repository import USDA_Ingredient_Repository
    from repository.USDA_Ingredient_Nutrient_Repository import (
        USDA_Ingredient_Nutrient_Repository,
    )
    from repository.USDA_Ingredient_Portion_Repository import (
        USDA_Ingredient_Portion_Repository,
    )
    from repository.USDA_Nutrient_Daily_Value_Repository import (
        USDA_Nutrient_Daily_Value_Repository,
    )

    from repository.Meal_Plan_Repository import Meal_Plan_Repository
    from repository.Meal_Plan_Meal_Repository import Meal_Plan_Meal_Repository
    from repository.Recipe_Ingredient_Repository import Recipe_Ingredient_Repository
    from repository.Recipe_Ingredient_Nutrient_Repository import (
        Recipe_Ingredient_Nutrient_Repository,
    )
    from repository.Dietary_Restriction_Repository import Dietary_Restriction_Repository
    from repository.Meal_Dietary_Restriction_Repository import (
        Meal_Dietary_Restriction_Repository,
    )
    from repository.Meal_Repository import Meal_Repository
    from repository.Snack_Repository import Snack_Repository
    from repository.Meal_Plan_Snack_Repository import Meal_Plan_Snack_Repository
    from service.Discount_Service import Discount_Service
    from service.Continuity_Service import Continuity_Service
    from service.Meal_Service import Meal_Service
    from service.Dietary_Restriction_Service import Dietary_Restriction_Service
    from service.Meal_Dietary_Restriction_Service import (
        Meal_Dietary_Restriction_Service,
    )
    from service.Meal_Plan_Service import Meal_Plan_Service
    from service.Meal_Plan_Meal_Service import Meal_Plan_Meal_Service
    from service.Snack_Service import Snack_Service
    from service.Meal_Plan_Snack_Service import Meal_Plan_Snack_Service
    from service.Nutrient_Service import Nutrient_Service
    from service.Recipe_Ingredient_Service import Recipe_Ingredient_Service
    from service.Recipe_Ingredient_Nutrient_Service import (
        Recipe_Ingredient_Nutrient_Service,
    )
    from service.USDA_Ingredient_Nutrient_Service import (
        USDA_Ingredient_Nutrient_Service,
    )
    from service.USDA_Ingredient_Portion_Service import (
        USDA_Ingredient_Portion_Service,
    )
    from service.USDA_Ingredient_Service import USDA_Ingredient_Service
    from service.USDA_Nutrient_Daily_Value_Service import (
        USDA_Nutrient_Daily_Value_Service,
    )

    # Only for writing local meal data to json for continuity when initializing in production
    if env != "debug":
        return Response(status=401)

    Continuity_Service().write_data(
        nutrient_service=Nutrient_Service(
            nutrient_repository=Nutrient_Repository(db=db)
        ),
        usda_ingredient_service=USDA_Ingredient_Service(
            usda_ingredient_repository=USDA_Ingredient_Repository(db=db)
        ),
        usda_ingredient_nutrient_service=USDA_Ingredient_Nutrient_Service(
            usda_ingredient_nutrient_repository=USDA_Ingredient_Nutrient_Repository(
                db=db
            )
        ),
        usda_ingredient_portion_service=USDA_Ingredient_Portion_Service(
            usda_ingredient_portion_repository=USDA_Ingredient_Portion_Repository(db=db)
        ),
        usda_nutrient_daily_value_service=USDA_Nutrient_Daily_Value_Service(
            usda_nutrient_daily_value_repository=USDA_Nutrient_Daily_Value_Repository(
                db=db
            )
        ),
        dietary_restriction_service=Dietary_Restriction_Service(
            dietary_restriction_repository=Dietary_Restriction_Repository(db=db)
        ),
        meal_service=Meal_Service(meal_repository=Meal_Repository(db=db)),
        meal_dietary_restriction_service=Meal_Dietary_Restriction_Service(
            meal_dietary_restriction_repository=Meal_Dietary_Restriction_Repository(
                db=db
            )
        ),
        meal_plan_service=Meal_Plan_Service(
            meal_plan_repository=Meal_Plan_Repository(db=db)
        ),
        meal_plan_meal_service=Meal_Plan_Meal_Service(
            meal_plan_meal_repository=Meal_Plan_Meal_Repository(db=db)
        ),
        snack_service=Snack_Service(snack_repository=Snack_Repository(db=db)),
        meal_plan_snack_service=Meal_Plan_Snack_Service(
            meal_plan_snack_repository=Meal_Plan_Snack_Repository(db=db)
        ),
        recipe_ingredient_service=Recipe_Ingredient_Service(
            recipe_ingredient_repository=Recipe_Ingredient_Repository(db=db)
        ),
        recipe_ingredient_nutrient_service=Recipe_Ingredient_Nutrient_Service(
            recipe_ingredient_nutrient_repository=Recipe_Ingredient_Nutrient_Repository(
                db=db
            )
        ),
        discount_service=Discount_Service(
            discount_repository=Discount_Repository(db=db)
        ),
    )
    return Response(status=200)


@app.route("/api/continuity/initialize")
def continuity_initialize() -> Response:
    from sqlalchemy import create_engine
    from helpers.db.get_db_connection_string import get_db_connection_string
    from helpers.db.create_state_tax_rates import create_state_tax_rates
    from helpers.check_auth import check_auth
    from helpers.db.create_cogs import create_cogs
    from helpers.db.create_eating_disorder import create_eating_disorder
    from service.GCP_Secret_Manager_Service import GCP_Secret_Manager_Service

    # import repository
    from repository.Continuity_Repository import Continuity_Repository
    from repository.Discount_Repository import Discount_Repository
    from repository.Imperial_Unit_Repository import Imperial_Unit_Repository
    from repository.Nutrient_Repository import Nutrient_Repository
    from repository.USDA_Ingredient_Repository import USDA_Ingredient_Repository
    from repository.USDA_Ingredient_Nutrient_Repository import (
        USDA_Ingredient_Nutrient_Repository,
    )
    from repository.USDA_Ingredient_Portion_Repository import (
        USDA_Ingredient_Portion_Repository,
    )
    from repository.USDA_Nutrient_Daily_Value_Repository import (
        USDA_Nutrient_Daily_Value_Repository,
    )

    from repository.Meal_Plan_Repository import Meal_Plan_Repository
    from repository.Meal_Plan_Meal_Repository import Meal_Plan_Meal_Repository
    from repository.Meal_Plan_Snack_Repository import Meal_Plan_Snack_Repository
    from repository.Recipe_Ingredient_Repository import Recipe_Ingredient_Repository
    from repository.Recipe_Ingredient_Nutrient_Repository import (
        Recipe_Ingredient_Nutrient_Repository,
    )
    from repository.Meal_Repository import Meal_Repository
    from repository.Snack_Repository import Snack_Repository
    from repository.Meal_Dietary_Restriction_Repository import (
        Meal_Dietary_Restriction_Repository,
    )
    from repository.Dietary_Restriction_Repository import Dietary_Restriction_Repository

    db_username = os.getenv("DB_USER") or GCP_Secret_Manager_Service().get_secret(
        "DB_USER"
    )

    db_password = os.getenv("DB_PASSWORD") or GCP_Secret_Manager_Service().get_secret(
        "DB_PASSWORD"
    )

    live_db_string = os.getenv("DB_STRING") or get_db_connection_string(
        username=db_username, password=db_password, db_name="nourishdb"
    )

    if not check_auth(env=env, db_password=db_password, request=request):
        return Response(status=401)

    db_engine = create_engine(live_db_string)
    db.drop_all()
    db.create_all()
    # initialize_db(
    #     db_engine=db_engine,
    #     drop_tables=True,
    # )
    create_state_tax_rates(db=db)
    create_cogs(db=db)
    create_eating_disorder(db=db)
    Continuity_Repository().initialize_meal_data(
        imperial_unit_repository=Imperial_Unit_Repository(engine=db_engine),
        nutrient_repository=Nutrient_Repository(engine=db_engine),
        usda_ingredient_repository=USDA_Ingredient_Repository(engine=db_engine),
        usda_ingredient_nutrient_repository=USDA_Ingredient_Nutrient_Repository(
            engine=db_engine
        ),
        usda_ingredient_portion_repository=USDA_Ingredient_Portion_Repository(
            engine=db_engine
        ),
        usda_nutrient_daily_value_repository=USDA_Nutrient_Daily_Value_Repository(
            engine=db_engine
        ),
        dietary_restriction_repository=Dietary_Restriction_Repository(engine=db_engine),
        meal_repository=Meal_Repository(engine=db_engine),
        snack_repository=Snack_Repository(engine=db_engine),
        meal_dietary_restriction_repository=Meal_Dietary_Restriction_Repository(
            engine=db_engine
        ),
        meal_plan_repository=Meal_Plan_Repository(engine=db_engine),
        meal_plan_meal_repository=Meal_Plan_Meal_Repository(engine=db_engine),
        meal_plan_snack_repository=Meal_Plan_Snack_Repository(engine=db_engine),
        recipe_ingredient_repository=Recipe_Ingredient_Repository(engine=db_engine),
        recipe_ingredient_nutrient_repository=Recipe_Ingredient_Nutrient_Repository(
            engine=db_engine
        ),
        discount_repository=Discount_Repository(engine=db_engine),
    )

    return Response(status=200)


@app.route("/api/email/sign_up", methods=["POST"])
def sign_up_email() -> Response:
    from dto.Staged_Client_DTO import Staged_Client_DTO
    from service.Email_Service import Email_Service
    from service.GCP_Secret_Manager_Service import GCP_Secret_Manager_Service

    staged_client = Staged_Client_DTO(staged_client_json=json.loads(request.data))
    Email_Service(
        gcp_secret_manager_service=GCP_Secret_Manager_Service()
    ).send_sign_up_email(staged_client=staged_client)
    return Response(status=200)


@app.route("/api/email/sign_up_confirmation/staged_client", methods=["POST"])
def sign_up_email_confirmation_client() -> Response:
    from dto.Staged_Client_DTO import Staged_Client_DTO
    from service.Email_Service import Email_Service
    from service.GCP_Secret_Manager_Service import GCP_Secret_Manager_Service
    from tzlocal import get_localzone

    staged_client = Staged_Client_DTO(staged_client_json=json.loads(request.data))
    dt = datetime.now()
    local_tz = get_localzone()
    local_dt = dt.astimezone(local_tz)
    delivery_date = local_dt
    cutoff_date = local_dt
    Email_Service(
        gcp_secret_manager_service=GCP_Secret_Manager_Service()
    ).send_confirmation_email(
        user_type="Client",
        user=staged_client,
        delivery_date=delivery_date,
        cutoff_date=cutoff_date,
        tracking_url="https://www.google.com",
    )
    return Response(status=200)


@app.route("/api/email/sign_up_confirmation/dietitian", methods=["POST"])
def sign_up_email_confirmation_dietitian() -> Response:
    from dto.Dietitian_DTO import Dietitian_DTO
    from service.Email_Service import Email_Service
    from service.GCP_Secret_Manager_Service import GCP_Secret_Manager_Service
    from tzlocal import get_localzone

    dietitian = Dietitian_DTO(
        dietitian_json=json.loads(request.data),
    )
    dt = datetime.now()
    local_tz = get_localzone()
    local_dt = dt.astimezone(local_tz)
    delivery_date = local_dt
    cutoff_date = local_dt
    Email_Service(
        gcp_secret_manager_service=GCP_Secret_Manager_Service()
    ).send_confirmation_email(
        user_type="Dietitian",
        user=dietitian,
        delivery_date=delivery_date,
        cutoff_date=cutoff_date,
        tracking_url="https://www.google.com",
    )
    return Response(status=200)


@app.route("/api/email/sign_up_reminder", methods=["POST"])
def sign_up_email_reminder() -> Response:
    from dto.Staged_Client_DTO import Staged_Client_DTO
    from service.Email_Service import Email_Service
    from service.GCP_Secret_Manager_Service import GCP_Secret_Manager_Service

    staged_client = Staged_Client_DTO(staged_client_json=json.loads(request.data))

    Email_Service(
        gcp_secret_manager_service=GCP_Secret_Manager_Service()
    ).send_sign_up_reminder_email(staged_client=staged_client)
    return Response(status=200)


@app.route("/api/test_dietetic", methods=["POST"])
def validate_dietetic_registration_number() -> Response:
    import requests

    dietetic_registration_number = json.loads(request.data)
    headers = {"Content-Type": "application/json"}
    response = requests.post(
        "https://secure.eatright.org/v14pgmlib/lansaweb?w=CDRVFYS&r=CREDSEARCH&vlweb=1&part=prd&lang=ENG&_T=1683030503817",
        json={
            "webroutine": {"fields": {"CRID#": {"value": dietetic_registration_number}}}
        },
        headers=headers,
    )
    response_data = response.json()
    entries = response_data["webroutine"]["lists"]["CREDCUST"]["entries"]
    if len(entries) > 0:
        return Response(status=200)
    else:
        return Response(status=404)


@app.route("/api/usda_ingredient_portion", methods=["POST", "PUT"])
def usda_ingredient_portion() -> Response:
    if request.method == "POST":
        from repository.USDA_Ingredient_Portion_Repository import (
            USDA_Ingredient_Portion_Repository,
        )
        from repository.USDA_Ingredient_Repository import USDA_Ingredient_Repository
        from service.USDA_Ingredient_Service import USDA_Ingredient_Service
        from service.USDA_Ingredient_Portion_Service import (
            USDA_Ingredient_Portion_Service,
        )
        from dto.USDA_Ingredient_Portion_DTO import USDA_Ingredient_Portion_DTO

        portion_data = json.loads(request.data)

        portion_json = {
            "id": portion_data["portion_id"],
            "usda_ingredient_id": portion_data["usda_ingredient_id"],
            "fda_portion_id": portion_data["fda_portion_id"],
            "non_metric_unit": portion_data["non_metric_unit"],
            # Grams to be calculated using standard portion size * multiplier, unless usda_data_type is Branded
            "grams_per_non_metric_unit": portion_data["grams_per_non_metric_unit"],
            "portion_description": portion_data["portion_description"],
            "is_imperial": portion_data["is_imperial"],
            # usda data type will be harvested from database
            "usda_data_type": "",
            "custom_value": portion_data["custom_value"],
            "multiplier": portion_data["multiplier"],
        }
        usda_portion_dto = USDA_Ingredient_Portion_DTO(
            usda_ingredient_portion_json=portion_json
        )
        usda_ingredient = USDA_Ingredient_Service(
            usda_ingredient_repository=USDA_Ingredient_Repository(db=db)
        ).get_usda_ingredient(usda_ingredient_id=usda_portion_dto.usda_ingredient_id)
        usda_portion_dto.usda_data_type = usda_ingredient.usda_data_type
        USDA_Ingredient_Portion_Service(
            usda_ingredient_portion_repository=USDA_Ingredient_Portion_Repository(db=db)
        ).create_usda_ingredient_portion(usda_ingredient_portion_dto=usda_portion_dto)
        return Response(status=201)
    elif request.method == "PUT":
        from repository.USDA_Ingredient_Portion_Repository import (
            USDA_Ingredient_Portion_Repository,
        )
        from repository.USDA_Ingredient_Repository import USDA_Ingredient_Repository
        from service.USDA_Ingredient_Service import USDA_Ingredient_Service
        from service.USDA_Ingredient_Portion_Service import (
            USDA_Ingredient_Portion_Service,
        )
        from dto.USDA_Ingredient_Portion_DTO import USDA_Ingredient_Portion_DTO

        portion_json = json.loads(request.data)

        usda_ingredient = USDA_Ingredient_Service(
            usda_ingredient_repository=USDA_Ingredient_Repository(db=db)
        ).get_usda_ingredient(usda_ingredient_id=portion_json["usda_ingredient_id"])
        USDA_Ingredient_Portion_Service(
            usda_ingredient_portion_repository=USDA_Ingredient_Portion_Repository(db=db)
        ).update_usda_ingredient_portion(usda_ingredient_portion_data=portion_json)
        return Response(status=201)
    else:
        return Response(status=405)


@app.route("/api/usda_ingredient/<string:usda_ingredient_id>", methods=["DELETE"])
@app.route(
    "/api/usda_ingredient", defaults={"usda_ingredient_id": None}, methods=["POST"]
)
def usda_ingredient(usda_ingredient_id: Optional[UUID]) -> Response:
    from models import USDA_api_key
    from repository.Imperial_Unit_Repository import Imperial_Unit_Repository
    from repository.Nutrient_Repository import Nutrient_Repository
    from repository.USDA_Ingredient_Repository import USDA_Ingredient_Repository
    from repository.USDA_Ingredient_Portion_Repository import (
        USDA_Ingredient_Portion_Repository,
    )
    from repository.USDA_Ingredient_Nutrient_Repository import (
        USDA_Ingredient_Nutrient_Repository,
    )
    from service.USDA_API_Service import USDA_API_Service
    from service.Nutrient_Service import Nutrient_Service
    from service.Imperial_Unit_Service import Imperial_Unit_Service
    from service.USDA_Ingredient_Service import USDA_Ingredient_Service
    from service.USDA_Ingredient_Portion_Service import USDA_Ingredient_Portion_Service
    from service.USDA_Ingredient_Nutrient_Service import (
        USDA_Ingredient_Nutrient_Service,
    )
    from dto.USDA_Nutrient_Mapper_DTO import USDA_Nutrient_Mapper_DTO

    if request.method == "POST":
        imperial_units = Imperial_Unit_Service(
            imperial_unit_repository=Imperial_Unit_Repository(db=db)
        ).get_imperial_units()
        nutrients = Nutrient_Service(
            nutrient_repository=Nutrient_Repository(db=db)
        ).get_nutrients()
        usda_ingredient = json.loads(request.data)
        fdc_id = usda_ingredient["fdc_id"]
        usda_ingredient_id = usda_ingredient["id"]
        usda_ingredient_name = usda_ingredient["name"]
        usda_ingredient_data = USDA_API_Service(
            USDA_api_key=USDA_api_key
        ).get_ingredient(fdc_id=fdc_id)
        mapped_usda_ingredient_data = USDA_Nutrient_Mapper_DTO(
            usda_ingredient_id=usda_ingredient_id,
            usda_ingredient_name=usda_ingredient_name,
            fdc_id=fdc_id,
            usda_ingredient_data=usda_ingredient_data,
            nutrients_list=nutrients,
            imperial_units=imperial_units,
        )

        USDA_Ingredient_Service(
            usda_ingredient_repository=USDA_Ingredient_Repository(db=db)
        ).create_usda_ingredient(usda_nutrient_mapper_dto=mapped_usda_ingredient_data)

        USDA_Ingredient_Nutrient_Service(
            usda_ingredient_nutrient_repository=USDA_Ingredient_Nutrient_Repository(
                db=db
            )
        ).create_usda_ingredient_nutrients(
            usda_ingredient_nutrient_dtos=mapped_usda_ingredient_data.nutrients
        )

        for portion_dto in mapped_usda_ingredient_data.portions:
            USDA_Ingredient_Portion_Service(
                usda_ingredient_portion_repository=USDA_Ingredient_Portion_Repository(
                    db=db
                )
            ).create_usda_ingredient_portion(usda_ingredient_portion_dto=portion_dto)

        return Response(status=201)

    elif request.method == "DELETE" and usda_ingredient_id is not None:
        from helpers.db.wipe_all_usda_ingredient_related_data import (
            wipe_all_usda_ingredient_related_data,
        )

        wipe_all_usda_ingredient_related_data(
            db=db, usda_ingredient_id=usda_ingredient_id
        )
        return Response(status=200)


@app.route("/api/webhook/weekly_update", methods=["POST"])
def weekly_update() -> Response:
    import base64
    from repository.Meal_Subscription_Repository import Meal_Subscription_Repository
    from repository.Scheduled_Order_Meal_Repository import (
        Scheduled_Order_Meal_Repository,
    )
    from repository.Schedule_Meal_Repository import Schedule_Meal_Repository
    from service.GCP_Secret_Manager_Service import GCP_Secret_Manager_Service
    from service.Date_Service import Date_Service
    from service.Meal_Subscription_Service import Meal_Subscription_Service
    from service.Scheduled_Order_Meal_Service import Scheduled_Order_Meal_Service
    from service.Schedule_Meal_Service import Schedule_Meal_Service

    base_64_auth_credentials: str | None = request.headers.get("Authorization").split(
        " "
    )[1]
    base64_bytes: bytes = base_64_auth_credentials.encode("ascii")
    message_bytes: bytes = base64.b64decode(base64_bytes)
    message: str = message_bytes.decode("ascii")
    username: str = message.split(":")[0]
    password: str = message.split(":")[1]
    if (
        os.getenv("WEBHOOK_USR")
        or GCP_Secret_Manager_Service().get_secret("WEBHOOK_USR")
    ) == username and (
        os.getenv("WEBHOOK_PWD")
        or GCP_Secret_Manager_Service().get_secret("WEBHOOK_PWD") == password
    ):
        # Create new scheduled order meals for the 5 weeks in the future
        Meal_Subscription_Service(
            meal_subscription_repository=Meal_Subscription_Repository(db=db)
        ).refresh_meal_subscriptions(
            scheduled_order_meal_service=Scheduled_Order_Meal_Service(
                scheduled_order_meal_repository=Scheduled_Order_Meal_Repository(db=db)
            ),
            schedule_meal_service=Schedule_Meal_Service(
                schedule_meal_repository=Schedule_Meal_Repository(db=db)
            ),
            date_service=Date_Service(),
        )
        return Response(status=204)
    else:
        return Response(status=401)


@app.route("/api/webhook/email/order_summary/<int:email_number>", methods=["POST"])
def email_webhook(email_number: int) -> Response:
    from repository.Meal_Subscription_Invoice_Repository import (
        Meal_Subscription_Invoice_Repository,
    )
    from service.Extended_Meal_Subscription_Invoice_Service import (
        Extended_Meal_Subscription_Invoice_Service,
    )
    from service.Date_Service import Date_Service
    from service.Email_Service import Email_Service
    from service.GCP_Secret_Manager_Service import GCP_Secret_Manager_Service
    import base64

    base_64_auth_credentials: str | None = request.headers.get("Authorization").split(
        " "
    )[1]
    base64_bytes: bytes = base_64_auth_credentials.encode("ascii")
    message_bytes: bytes = base64.b64decode(base64_bytes)
    message: str = message_bytes.decode("ascii")
    username: str = message.split(":")[0]
    password: str = message.split(":")[1]
    if (
        os.getenv("WEBHOOK_USR")
        or GCP_Secret_Manager_Service().get_secret("WEBHOOK_USR")
    ) == username and (
        os.getenv("WEBHOOK_PWD")
        or GCP_Secret_Manager_Service().get_secret("WEBHOOK_PWD") == password
    ):
        current_week_delivery_date = Date_Service().get_current_week_delivery_date()

        # Get recently created invoices for delivery this week
        current_week_invoices = Extended_Meal_Subscription_Invoice_Service(
            meal_subscription_invoice_repository=Meal_Subscription_Invoice_Repository(
                db=db
            )
        ).get_upcoming_extended_meal_subscription_invoices(
            delivery_date=current_week_delivery_date
        )

        first_week_email_datetime = Date_Service().get_first_email_datetime()
        Email_Service(
            gcp_secret_manager_service=GCP_Secret_Manager_Service()
        ).send_upcoming_deliveries_email(
            delivery_date=datetime.utcfromtimestamp(current_week_delivery_date).replace(
                tzinfo=timezone.utc
            ),
            first_email_datetime=first_week_email_datetime,
            meal_subscription_invoices=current_week_invoices,
            email_number=email_number,
        )
        return Response(status=204)
    else:
        return Response(status=401)


@app.route("/api/webhook/stripe/invoice", methods=["POST"])
def stripe_webhook() -> Response:
    from models import stripe_invoice_endpoint_secret
    from stripe import Event

    event = None
    payload: bytes = request.data

    try:
        event = json.loads(payload)
    except:
        print("⚠️  Webhook error while parsing basic request." + str(e))
        return Response(status=400)
    if stripe_invoice_endpoint_secret:
        # Only verify the event if there is an endpoint secret defined
        # Otherwise use the basic event deserialized with json
        sig_header: str | None = request.headers.get("stripe-signature")
        try:
            event: Event = stripe.Webhook.construct_event(
                payload, sig_header, stripe_invoice_endpoint_secret
            )
        except stripe.error.SignatureVerificationError as e:
            print("⚠️  Webhook signature verification failed." + str(e))
            return Response(status=400)

    if event and event["type"] == "invoice.paid":
        from repository.Client_Repository import Client_Repository
        from repository.Meal_Subscription_Repository import Meal_Subscription_Repository
        from repository.Meal_Subscription_Invoice_Repository import (
            Meal_Subscription_Invoice_Repository,
        )
        from repository.Schedule_Meal_Repository import Schedule_Meal_Repository
        from repository.Schedule_Snack_Repository import Schedule_Snack_Repository
        from repository.Scheduled_Order_Meal_Repository import (
            Scheduled_Order_Meal_Repository,
        )
        from repository.Scheduled_Order_Snack_Repository import (
            Scheduled_Order_Snack_Repository,
        )
        from repository.Staged_Client_Repository import Staged_Client_Repository
        from repository.Order_Meal_Repository import Order_Meal_Repository
        from repository.Order_Snack_Repository import Order_Snack_Repository
        from repository.Meal_Shipment_Repository import Meal_Shipment_Repository
        from repository.COGS_Repository import COGS_Repository

        from service.Staged_Client_Service import Staged_Client_Service
        from service.Client_Service import Client_Service

        from service.Schedule_Meal_Service import Schedule_Meal_Service
        from service.Schedule_Snack_Service import Schedule_Snack_Service
        from service.Scheduled_Order_Meal_Service import Scheduled_Order_Meal_Service
        from service.Scheduled_Order_Snack_Service import Scheduled_Order_Snack_Service

        from service.Meal_Subscription_Service import Meal_Subscription_Service
        from service.Meal_Subscription_Invoice_Service import (
            Meal_Subscription_Invoice_Service,
        )
        from service.Order_Meal_Service import Order_Meal_Service
        from service.Order_Snack_Service import Order_Snack_Service

        from service.Date_Service import Date_Service
        from service.Shippo_Service import Shippo_Service
        from service.Stripe_Service import Stripe_Service
        from service.Order_Calc_Service import Order_Calc_Service
        from service.COGS_Service import COGS_Service
        from domain.Meal_Subscription_Domain import Meal_Subscription_Domain
        from domain.Scheduled_Order_Meal_Domain import Scheduled_Order_Meal_Domain
        from domain.Scheduled_Order_Snack_Domain import Scheduled_Order_Snack_Domain

        from domain.Order_Meal_Domain import Order_Meal_Domain
        from domain.Order_Snack_Domain import Order_Snack_Domain

        from dto.Order_Meal_DTO import Order_Meal_DTO
        from dto.Order_Snack_DTO import Order_Snack_DTO
        from dto.Meal_Subscription_Invoice_DTO import Meal_Subscription_Invoice_DTO
        from datetime import datetime

        stripe_invoice_id = event["data"]["object"]["id"]
        stripe_subscription_id = event["data"]["object"]["subscription"]
        stripe_payment_intent_id = event["data"]["object"]["payment_intent"]

        meal_subscription: Optional[
            Meal_Subscription_Domain
        ] = Meal_Subscription_Service(
            meal_subscription_repository=Meal_Subscription_Repository(db=db)
        ).get_meal_subscription(
            stripe_subscription_id=stripe_subscription_id
        )

        if not meal_subscription:
            return Response(status=404)

        staged_client = Staged_Client_Service(
            staged_client_repository=Staged_Client_Repository(db=db)
        ).get_staged_client(staged_client_id=meal_subscription.client_id)

        # Modifying stripe subscription will generate a new invoice with a null payment intent id
        if (
            staged_client.account_created is True
            and stripe_payment_intent_id is not None
        ):
            meal_subscription_invoice_dto = Meal_Subscription_Invoice_DTO()
            meal_subscription_invoice_dto.datetime = datetime.now(
                timezone.utc
            ).timestamp()
            num_meals = len(
                Schedule_Meal_Service(
                    schedule_meal_repository=Schedule_Meal_Repository(db=db)
                ).get_schedule_meals(meal_subscription_id=meal_subscription.id)
            )
            schedule_snacks = Schedule_Snack_Service(
                schedule_snack_repository=Schedule_Snack_Repository(db=db)
            ).get_schedule_snacks(meal_subscription_id=meal_subscription.id)
            if schedule_snacks:
                num_snacks = len(schedule_snacks)
            else:
                num_snacks = 0

            cost_per_meal = COGS_Service(
                cogs_repository=COGS_Repository(db=db)
            ).get_meal_cost(
                num_meals=num_meals,
                num_snacks=num_snacks,
                shipping_rate=meal_subscription.shipping_rate,
            )
            meal_price = COGS_Service(
                cogs_repository=COGS_Repository(db=db)
            ).get_meal_price(meal_cost=cost_per_meal)

            num_items = COGS_Service(
                cogs_repository=COGS_Repository(db=db)
            ).get_num_items(num_meals=num_meals, num_snacks=num_snacks)

            shipping_cost = COGS_Service(
                cogs_repository=COGS_Repository(db=db)
            ).get_shipping_cost(
                num_meals=num_meals,
                num_snacks=num_snacks,
                shipping_rate=meal_subscription.shipping_rate,
            )
            new_invoice = Meal_Subscription_Invoice_Service(
                meal_subscription_invoice_repository=Meal_Subscription_Invoice_Repository(
                    db=db
                )
            ).create_meal_subscription_invoice_from_stripe_event(
                meal_subscription_invoice_dto=meal_subscription_invoice_dto,
                meal_subscription=meal_subscription,
                stripe_invoice_id=stripe_invoice_id,
                stripe_payment_intent_id=stripe_payment_intent_id,
                meal_price=meal_price,
                shipping_cost=shipping_cost,
                num_items=num_items,
                order_calc_service=Order_Calc_Service(),
            )

            client = Client_Service(
                client_repository=Client_Repository(db=db)
            ).get_client(client_id=meal_subscription.client_id)

            Shippo_Service().create_shipment(
                meal_subscription_invoice_id=new_invoice.id,
                client=client,
                meal_shipment_repository=Meal_Shipment_Repository(db=db),
            )

            # Get scheduled order meals for this week
            this_weeks_scheduled_order_meals: list[
                Scheduled_Order_Meal_Domain
            ] = Scheduled_Order_Meal_Service(
                scheduled_order_meal_repository=Scheduled_Order_Meal_Repository(db=db)
            ).get_scheduled_order_meals_for_week(
                meal_subscription_id=meal_subscription.id,
                delivery_date=Date_Service().get_current_week_delivery_date(),
            )

            # Create new order meals for invoice
            for scheduled_order_meal in this_weeks_scheduled_order_meals:
                order_meal_id = uuid.uuid4()
                scheduled_order_meal_id = scheduled_order_meal.id

                # DTO is expecting strings for id's
                order_meal_json = {
                    "id": str(order_meal_id),
                    "scheduled_order_meal_id": str(scheduled_order_meal_id),
                    "meal_subscription_invoice_id": str(new_invoice.id),
                }

                order_meal_dto = Order_Meal_DTO(order_meal_json=order_meal_json)
                order_meal_domain = Order_Meal_Domain(order_meal_object=order_meal_dto)
                Order_Meal_Service(
                    order_meal_repository=Order_Meal_Repository(db=db)
                ).create_order_meal(order_meal_domain=order_meal_domain)

            # Get scheduled order snacks for this week
            this_weeks_scheduled_order_snacks: list[
                Scheduled_Order_Snack_Domain
            ] = Scheduled_Order_Snack_Service(
                scheduled_order_snack_repository=Scheduled_Order_Snack_Repository(db=db)
            ).get_scheduled_order_snacks_for_week(
                meal_subscription_id=meal_subscription.id,
                delivery_date=Date_Service().get_current_week_delivery_date(),
            )

            # Create new order snacks for invoice
            for scheduled_order_snack in this_weeks_scheduled_order_snacks:
                order_snack_id = uuid.uuid4()
                scheduled_order_snack_id = scheduled_order_snack.id
                order_snack_json = {
                    "id": str(order_snack_id),
                    "scheduled_order_snack_id": str(scheduled_order_snack_id),
                    "meal_subscription_invoice_id": str(new_invoice.id),
                }

                order_snack_dto = Order_Snack_DTO(order_snack_json=order_snack_json)
                order_snack_domain = Order_Snack_Domain(
                    order_snack_object=order_snack_dto
                )
                Order_Snack_Service(
                    order_snack_repository=Order_Snack_Repository(db=db)
                ).create_order_snack(order_snack_domain=order_snack_domain)

        # Invoice created when client first signs up
        elif staged_client.account_created is False:
            from service.Staged_Client_Service import Staged_Client_Service
            from service.Meal_Subscription_Invoice_Service import (
                Meal_Subscription_Invoice_Service,
            )

            first_meal_subscription_invoice = Meal_Subscription_Invoice_Service(
                meal_subscription_invoice_repository=Meal_Subscription_Invoice_Repository(
                    db=db
                )
            ).get_first_meal_subscription_invoice(
                meal_subscription_id=meal_subscription.id
            )
            Meal_Subscription_Invoice_Service(
                meal_subscription_invoice_repository=Meal_Subscription_Invoice_Repository(
                    db=db
                )
            ).update_first_meal_subscription_invoice(
                meal_subscription_invoice_id=first_meal_subscription_invoice.id,
                stripe_invoice_id=stripe_invoice_id,
                stripe_payment_intent_id=stripe_payment_intent_id,
            )
            # Apply discount to invoice for the first week of meals because it was paid up front during account creation
            Stripe_Service().apply_coupon(stripe_subscription_id=stripe_subscription_id)

            # Update staged client account status to created
            Staged_Client_Service(
                staged_client_repository=Staged_Client_Repository(db=db)
            ).update_staged_client_account_status(staged_client_id=staged_client.id)
        else:
            print("Unhandled invoice event {}".format(event["type"]))

    else:
        # Unexpected event type, payment failes etc... lots of work to be done here
        print("Unhandled event type {}".format(event["type"]))

    return Response(status=204)


@app.route("/api/delivery_date", methods=["GET"])
# @requires_auth
def delivery_date() -> None:
    from service.Date_Service import Date_Service
    from flask import jsonify

    current_week_delivery_date = Date_Service().get_current_week_delivery_date()
    current_week_cutoff_date = Date_Service().get_current_week_cutoff(
        current_delivery_date=current_week_delivery_date
    )
    sign_up = request.headers.get("sign-up")
    # If the cutoff for this week has passed, update the delivery date to next week
    # Then update the cutoff date to next week
    if sign_up and current_week_cutoff_date < datetime.now(timezone.utc).timestamp():
        current_week_delivery_date = Date_Service().get_next_week_date(
            current_week_delivery_date
        )
        current_week_cutoff_date = Date_Service().get_next_week_date(
            current_week_cutoff_date
        )

    upcoming_delivery_dates = Date_Service().get_upcoming_delivery_dates(
        current_week_delivery_date=current_week_delivery_date,
    )
    upcoming_delivery_cutoff_dates = Date_Service().get_upcoming_cutoff_delivery_dates(
        current_week_cutoff_date=current_week_cutoff_date,
    )

    return jsonify(
        {
            "upcoming_delivery_dates": upcoming_delivery_dates,
            "upcoming_cutoff_dates": upcoming_delivery_cutoff_dates,
        }
    )


@app.route("/api/staged_client/reminder", methods=["GET"])
def send_reminder() -> Response:
    from service.Staged_Client_Service import Staged_Client_Service
    from service.Email_Service import Email_Service
    from service.GCP_Secret_Manager_Service import GCP_Secret_Manager_Service
    from repository.Staged_Client_Repository import Staged_Client_Repository

    staged_client_id: str | None = request.headers.get("staged-client-id")
    staged_client = Staged_Client_Service(
        staged_client_repository=Staged_Client_Repository(db=db)
    ).get_staged_client(staged_client_id=staged_client_id)
    Email_Service(
        gcp_secret_manager_service=GCP_Secret_Manager_Service()
    ).send_sign_up_reminder_email(staged_client=staged_client)
    return Response(status=204)


@app.route("/api/dietitian", methods=["POST"])
def dietitian() -> Response | Response:
    from repository.Meal_Repository import Meal_Repository
    from repository.Meal_Sample_Repository import Meal_Sample_Repository
    from service.Dietitian_Service import Dietitian_Service
    from service.Email_Service import Email_Service
    from service.GCP_Secret_Manager_Service import GCP_Secret_Manager_Service
    from service.Meal_Service import Meal_Service
    from service.Meal_Sample_Service import Meal_Sample_Service
    from repository.Dietitian_Repository import Dietitian_Repository
    from dto.Dietitian_DTO import Dietitian_DTO
    from dto.Meal_Sample_DTO import Meal_Sample_DTO

    if request.method == "POST":
        requested_dietitian = json.loads(request.data)
        requested_dietitian_dto = Dietitian_DTO(
            dietitian_json=requested_dietitian,
        )
        created_dietitian_domain = Dietitian_Service(
            dietitian_repository=Dietitian_Repository(db=db)
        ).create_dietitian(dietitian_dto=requested_dietitian_dto)
        Email_Service(
            gcp_secret_manager_service=GCP_Secret_Manager_Service(),
        ).send_confirmation_email(user_type="Dietitian", user=created_dietitian_domain)
        if created_dietitian_domain.got_sample:
            dietitian_meal_sample_dtos = []
            meal_samples = Meal_Service(
                meal_repository=Meal_Repository(db=db)
            ).get_meal_samples()
            for meal in meal_samples:
                meal_sample_json = {
                    "id": uuid.uuid4(),
                    "meal_id": meal.id,
                    "dietitian_id": created_dietitian_domain.id,
                }
                dietitian_meal_sample_dto = Meal_Sample_DTO(
                    meal_sample_json=meal_sample_json
                )
                dietitian_meal_sample_dtos.append(dietitian_meal_sample_dto)
            Meal_Sample_Service(
                meal_sample_repository=Meal_Sample_Repository(db=db)
            ).create_meal_samples(meal_sample_dtos=dietitian_meal_sample_dtos)

        Email_Service(
            gcp_secret_manager_service=GCP_Secret_Manager_Service(),
        ).send_new_user_sign_up_notification(
            first_name="Peter",
            email="peterdriscoll@cherahealth.com",
            user_type="Dietitian",
            user=created_dietitian_domain,
            env=env,
        )

        dietitian_dto = Dietitian_DTO(
            dietitian_domain=created_dietitian_domain,
        )
        serialized_dietitian_dto = dietitian_dto.serialize()
        return jsonify(serialized_dietitian_dto), 201
    else:
        return Response(status=405)


@app.route("/api/shippo/meal_sample_shipment", methods=["POST"])
def create_meal_sample_shipment() -> Response:
    from repository.Meal_Sample_Shipment_Repository import (
        Meal_Sample_Shipment_Repository,
    )
    from service.GCP_Secret_Manager_Service import GCP_Secret_Manager_Service
    from service.Shippo_Service import Shippo_Service
    from dto.Dietitian_DTO import Dietitian_DTO

    request_data = json.loads(request.data)
    dietitian = Dietitian_DTO(
        dietitian_json=request_data["dietitian"],
    )
    shipping_address = request_data["shipping_address"]
    Shippo_Service().create_sample_shipment(
        dietitian=dietitian,
        shipping_address=shipping_address,
        meal_sample_shipment_repository=Meal_Sample_Shipment_Repository(db=db),
    )
    return Response(status=200)


@app.route("/api/email/meal_sample", methods=["POST"])
def sample_order_confirmation() -> Response:
    from repository.Meal_Repository import Meal_Repository
    from repository.Meal_Sample_Shipment_Repository import (
        Meal_Sample_Shipment_Repository,
    )
    from service.Meal_Service import Meal_Service
    from service.Meal_Sample_Shipment_Service import Meal_Sample_Shipment_Service
    from service.Email_Service import Email_Service
    from service.GCP_Secret_Manager_Service import GCP_Secret_Manager_Service
    from service.Date_Service import Date_Service
    from dto.Dietitian_DTO import Dietitian_DTO
    from tzlocal import get_localzone

    dietitian = Dietitian_DTO(
        dietitian_json=json.loads(request.data),
    )
    meal_samples = Meal_Service(
        meal_repository=Meal_Repository(db=db)
    ).get_meal_samples()
    meal_sample_names = [meal_sample.name for meal_sample in meal_samples]

    meal_sample_delivery_date_timestamp = (
        Date_Service().get_current_week_sample_delivery_date(
            today=datetime.now(timezone.utc)
        )
    )
    meal_sample_delivery_date = datetime.utcfromtimestamp(
        meal_sample_delivery_date_timestamp
    ).replace(tzinfo=timezone.utc)
    local_tz = get_localzone()
    local_dt = meal_sample_delivery_date.astimezone(local_tz)

    meal_sample_shipment = Meal_Sample_Shipment_Service(
        meal_sample_shipment_repository=Meal_Sample_Shipment_Repository(db=db)
    ).get_meal_sample_shipment(dietitian_id=dietitian.id)

    Email_Service(
        gcp_secret_manager_service=GCP_Secret_Manager_Service()
    ).send_sample_order_confirmation_email(
        dietitian=dietitian,
        delivery_date=local_dt,
        tracking_url=meal_sample_shipment.tracking_url,
        meal_sample_names=meal_sample_names,
    )
    return Response(status=200)


@app.route("/api/dietitian/<string:dietitian_email>", methods=["GET"])
def get_dietitian(dietitian_email: str) -> Response:
    from service.Dietitian_Service import Dietitian_Service
    from repository.Dietitian_Repository import Dietitian_Repository
    from domain.Dietitian_Domain import Dietitian_Domain
    from dto.Dietitian_DTO import Dietitian_DTO

    if request.method == "GET":
        dietitian_domain: Optional[Dietitian_Domain] = Dietitian_Service(
            dietitian_repository=Dietitian_Repository(db=db)
        ).get_dietitian(dietitian_email=dietitian_email)
        if dietitian_domain and dietitian_domain.active:
            dietitian_DTO = Dietitian_DTO(
                dietitian_domain=dietitian_domain,
            )
            return jsonify(dietitian_DTO.serialize()), 200
        else:
            return Response(status=404)
    else:
        return Response(status=405)


@app.route("/api/extended_client", methods=["GET"])
def extended_clients() -> Response:
    from service.Extended_Client_Service import Extended_Client_Service
    from repository.Client_Repository import Client_Repository
    from domain.Extended_Client_Domain import Extended_Client_Domain
    from dto.Extended_Client_DTO import Extended_Client_DTO

    if request.method == "GET":
        dietitian_id: str = request.args.get("dietitian_id")
        requested_extended_clients: Optional[
            list[Extended_Client_Domain]
        ] = Extended_Client_Service(
            client_repository=Client_Repository(db=db)
        ).get_extended_clients(
            dietitian_id=dietitian_id
        )
        if requested_extended_clients:
            requested_extended_client_dtos: list[Extended_Client_DTO] = [
                Extended_Client_DTO(extended_client_domain=x)
                for x in requested_extended_clients
            ]
            serialized_requested_extended_client_dtos = [
                x.serialize() for x in requested_extended_client_dtos
            ]
            return jsonify(serialized_requested_extended_client_dtos), 200
        else:
            return Response(status=204)
    else:
        return Response(status=405)


@app.route("/api/client/<string:client_email>", methods=["GET", "PUT"])
def update_client(client_email: str) -> Response:
    from repository.Client_Repository import Client_Repository
    from service.Client_Service import Client_Service
    from dto.Client_DTO import Client_DTO

    if request.method == "GET":
        requested_client = Client_Service(
            client_repository=Client_Repository(db=db)
        ).get_client(client_email=client_email)
        if requested_client and requested_client.active:
            client_DTO = Client_DTO(client_domain=requested_client)
            return jsonify(client_DTO.serialize()), 200
        else:
            return Response(status=404)
    elif request.method == "PUT":
        Client_Service(client_repository=Client_Repository(db=db)).deactivate_client(
            client_email=client_email
        )
        return Response(status=204)
    else:
        return Response(status=405)


@app.route("/api/client", methods=["GET", "POST", "PUT"])
def client() -> Response:
    from service.Client_Service import Client_Service
    from service.Email_Service import Email_Service
    from service.GCP_Secret_Manager_Service import GCP_Secret_Manager_Service
    from repository.Client_Repository import Client_Repository
    from domain.Client_Domain import Client_Domain
    from dto.Client_DTO import Client_DTO

    if request.method == "GET":
        dietitian_id: str = request.args.get("dietitian_id")
        requested_clients: list[Client_Domain] = Client_Service(
            client_repository=Client_Repository(db=db)
        ).get_clients(dietitian_id=dietitian_id)
        requested_client_dtos: list[Client_DTO] = [
            Client_DTO(client_domain=x) for x in requested_clients
        ]
        serialized_requested_client_dtos = [
            x.serialize() for x in requested_client_dtos
        ]
        return jsonify(serialized_requested_client_dtos), 200

    elif request.method == "POST":
        requested_client = json.loads(request.data)
        requested_client_dto = Client_DTO(client_json=requested_client)
        check_previous_client: Optional[Client_Domain] = Client_Service(
            client_repository=Client_Repository(db=db)
        ).get_client(client_id=requested_client_dto.id)
        if check_previous_client:
            returned_client = Client_Service(
                client_repository=Client_Repository(db=db)
            ).update_client(client_dto=requested_client_dto)
        else:
            returned_client = Client_Service(
                client_repository=Client_Repository(db=db)
            ).create_client(client_dto=requested_client_dto)

        Email_Service(
            gcp_secret_manager_service=GCP_Secret_Manager_Service(),
        ).send_new_user_sign_up_notification(
            first_name="Peter",
            email="peterdriscoll@cherahealth.com",
            user_type="Client",
            user=returned_client,
            env=env,
            zipcode=returned_client.zipcode,
        )
        returned_client_dto = Client_DTO(client_domain=returned_client)

        return jsonify(returned_client_dto.serialize()), 201

    elif request.method == "PUT":
        client_dto: Client_DTO = Client_DTO(client_json=json.loads(request.data))
        Client_Service(
            client_repository=Client_Repository(db=db)
        ).update_client_meal_plan(client_dto=client_dto)
        return Response(status=200)


@app.route("/api/stripe/invoice", methods=["GET"])
def get_stripe_invoice() -> Response:
    from service.Stripe_Service import Stripe_Service
    from repository.Client_Repository import Client_Repository

    if request.method == "GET":
        invoice_id: str = request.args.get("invoice_id")
        invoice = Stripe_Service().get_invoice(invoice_id=invoice_id)
        if invoice:
            return jsonify(invoice), 200
        else:
            return Response(status=204)
    else:
        return Response(status=405)


@app.route("/api/stripe/customer/<string:customer_id>", methods=["DELETE"])
def delete_stripe_invoice(customer_id: str) -> Response:
    from service.Stripe_Service import Stripe_Service

    if request.method == "DELETE":
        Stripe_Service().delete_customer(customer_id=customer_id)
        return Response(status=204)
    else:
        return Response(status=405)


@app.route("/api/stripe/subscription", methods=["POST", "PUT", "GET", "DELETE"])
def stripe_subscription_data() -> Response:
    from models import stripe_one_time_account_setup_fee
    from repository.COGS_Repository import COGS_Repository
    from service.COGS_Service import COGS_Service
    from service.Shippo_Service import Shippo_Service
    from service.Meal_Subscription_Service import Meal_Subscription_Service
    from service.Stripe_Service import Stripe_Service
    from service.Discount_Service import Discount_Service
    from service.Date_Service import Date_Service
    from repository.Discount_Repository import Discount_Repository
    from repository.Meal_Subscription_Repository import Meal_Subscription_Repository

    if request.method == "POST":
        stripe_subscription_data = json.loads(request.data)
        client_email: str = stripe_subscription_data["client_email"]
        number_of_meals: int = int(stripe_subscription_data["number_of_meals"])
        number_of_snacks: int = int(stripe_subscription_data["number_of_snacks"])
        zipcode: str = stripe_subscription_data["zipcode"]
        discount_code: str = stripe_subscription_data["discount_code"]
        prepaid: bool = stripe_subscription_data["prepaid"]

        discount = Discount_Service(
            discount_repository=Discount_Repository(db=db)
        ).verify_discount_code(discount_code=discount_code)

        shipping_rate = Shippo_Service().get_shipping_rate(zipcode=zipcode)

        cost_per_meal = COGS_Service(
            cogs_repository=COGS_Repository(db=db)
        ).get_meal_cost(
            num_meals=number_of_meals,
            num_snacks=number_of_snacks,
            shipping_rate=shipping_rate,
        )
        meal_price = COGS_Service(
            cogs_repository=COGS_Repository(db=db)
        ).get_meal_price(meal_cost=cost_per_meal)

        num_items = COGS_Service(cogs_repository=COGS_Repository(db=db)).get_num_items(
            num_meals=number_of_meals, num_snacks=number_of_snacks
        )

        client_stripe_data = Stripe_Service().create_stripe_subscription(
            num_items=num_items,
            meal_price=meal_price,
            client_email=client_email,
            stripe_one_time_account_setup_fee_price_id=stripe_one_time_account_setup_fee,
            date_service=Date_Service(),
            prepaid=prepaid,
            discount=discount,
        )
        return jsonify(client_stripe_data), 201
    elif request.method == "PUT":
        meal_subscription_id = request.args.get("meal_subscription_id")

        number_of_meals = int(request.headers.get("number-of-meals"))
        number_of_snacks = int(request.headers.get("number-of-snacks"))

        client_subscription = Meal_Subscription_Service(
            meal_subscription_repository=Meal_Subscription_Repository(db=db)
        ).get_meal_subscription(meal_subscription_id=meal_subscription_id)

        shipping_rate = client_subscription.shipping_rate

        cost_per_meal = COGS_Service(
            cogs_repository=COGS_Repository(db=db)
        ).get_meal_cost(
            num_meals=number_of_meals,
            num_snacks=number_of_snacks,
            shipping_rate=shipping_rate,
        )
        meal_price = COGS_Service(
            cogs_repository=COGS_Repository(db=db)
        ).get_meal_price(meal_cost=cost_per_meal)
        stripe_meal_price_id = Stripe_Service().get_price(
            meal_price=meal_price,
            recurring=True,
        )["price_id"]
        number_of_items = COGS_Service(
            cogs_repository=COGS_Repository(db=db)
        ).get_num_items(num_meals=number_of_meals, num_snacks=number_of_snacks)
        Stripe_Service().update_subscription(
            stripe_subscription_id=client_subscription.stripe_subscription_id,
            num_items=number_of_items,
            stripe_meal_price_id=stripe_meal_price_id,
        )
        return Response(status=204)

    elif request.method == "GET":
        stripe_subscription = Stripe_Service().get_subscription(
            stripe_subscription_id=request.args.get("stripe_subscription_id")
        )
        return jsonify(stripe_subscription), 200

    elif request.method == "DELETE":
        stripe_subscription_id = request.args.get("stripe_subscription_id")
        Stripe_Service().delete_subscription(
            stripe_subscription_id=stripe_subscription_id
        )
        return Response(status=204)
    else:
        return Response(status=405)


@app.route("/api/extended_staged_client", methods=["GET"])
def extended_staged_client() -> Response:
    from service.Extended_Staged_Client_Service import Extended_Staged_Client_Service
    from repository.Staged_Client_Repository import Staged_Client_Repository
    from domain.Extended_Staged_Client_Domain import Extended_Staged_Client_Domain
    from dto.Extended_Staged_Client_DTO import Extended_Staged_Client_DTO

    if request.method == "GET":
        dietitian_id: Optional[str] = request.args.get("dietitian_id")
        extended_staged_client_domains: Optional[
            list[Extended_Staged_Client_Domain]
        ] = Extended_Staged_Client_Service(
            staged_client_repository=Staged_Client_Repository(db=db)
        ).get_extended_staged_clients(
            dietitian_id=dietitian_id
        )
        if extended_staged_client_domains:
            extended_staged_client_DTOs: list[Extended_Staged_Client_DTO] = [
                Extended_Staged_Client_DTO(extended_staged_client_domain=x)
                for x in extended_staged_client_domains
            ]
            serialized_extended_staged_clients: list[dict] = [
                x.serialize() for x in extended_staged_client_DTOs
            ]
            return jsonify(serialized_extended_staged_clients), 200
        else:
            return Response(status=204)
    else:
        return Response(status=405)


@app.route("/api/staged_client/<string:staged_client_identifier>", methods=["GET"])
@app.route(
    "/api/staged_client",
    defaults={"staged_client_identifier": None},
    methods=["GET", "POST", "PUT"],
)
def staged_client(staged_client_identifier: Optional[str]) -> Response:
    from service.Staged_Client_Service import Staged_Client_Service
    from service.Email_Service import Email_Service
    from service.GCP_Secret_Manager_Service import GCP_Secret_Manager_Service
    from repository.Staged_Client_Repository import Staged_Client_Repository
    from domain.Staged_Client_Domain import Staged_Client_Domain
    from dto.Staged_Client_DTO import Staged_Client_DTO

    if request.method == "GET" and staged_client_identifier:
        staged_client: Optional[Staged_Client_Domain] = Staged_Client_Service(
            staged_client_repository=Staged_Client_Repository(db=db)
        ).get_staged_client(staged_client_email=staged_client_identifier)

        staged_client = Staged_Client_Service(
            staged_client_repository=Staged_Client_Repository(db=db)
        ).get_staged_client(staged_client_id=staged_client_identifier)
        if staged_client and staged_client.active:
            staged_client_dto = Staged_Client_DTO(staged_client_domain=staged_client)
            return jsonify(staged_client_dto.serialize()), 200
        else:
            return Response(status=404)

    elif request.method == "GET" and not staged_client_identifier:
        staged_client_email = request.args.get("email")
        if staged_client_email:
            staged_client = Staged_Client_Service(
                staged_client_repository=Staged_Client_Repository(db=db)
            ).get_staged_client(staged_client_id=staged_client_identifier)
            if staged_client and staged_client.active:
                staged_client_dto = Staged_Client_DTO(
                    staged_client_domain=staged_client
                )
                staged_client_dto
                return jsonify(staged_client_dto.serialize()), 200
            else:
                return Response(status=404)
        else:
            dietitian_id: Optional[str] = request.args.get("dietitian_id")
            staged_client_domains: list[Staged_Client_Domain] = Staged_Client_Service(
                staged_client_repository=Staged_Client_Repository(db=db)
            ).get_staged_clients(dietitian_id=dietitian_id)
            staged_client_DTOs: list[Staged_Client_DTO] = [
                Staged_Client_DTO(staged_client_domain=x) for x in staged_client_domains
            ]
            serialized_staged_clients: list[dict] = [
                x.serialize() for x in staged_client_DTOs
            ]
            return jsonify(serialized_staged_clients), 200

    elif request.method == "POST":
        staged_client_dto: Staged_Client_DTO = Staged_Client_DTO(
            staged_client_json=json.loads(request.data)
        )
        new_staged_client_domain = Staged_Client_Service(
            staged_client_repository=Staged_Client_Repository(db=db)
        ).create_staged_client(staged_client_dto=staged_client_dto)
        Email_Service(
            gcp_secret_manager_service=GCP_Secret_Manager_Service(),
        ).send_sign_up_email(staged_client=new_staged_client_domain)
        Email_Service(
            gcp_secret_manager_service=GCP_Secret_Manager_Service(),
        ).send_new_user_sign_up_notification(
            first_name="Peter",
            email="peterdriscoll@cherahealth.com",
            user_type="Staged_Client",
            user=new_staged_client_domain,
            env=env,
            zipcode=None,
        )
        return Response(status=201)

    elif request.method == "PUT":
        staged_client_dto: Staged_Client_DTO = Staged_Client_DTO(
            staged_client_json=json.loads(request.data)
        )
        Staged_Client_Service(
            staged_client_repository=Staged_Client_Repository(db=db)
        ).update_staged_client_meal_plan(staged_client_dto=staged_client_dto)
        return Response(status=204)
    else:
        return Response(status=405)


@app.route("/api/extended_usda_ingredient", methods=["GET"])
def extended_usda_ingredient() -> Response:
    from repository.USDA_Ingredient_Repository import USDA_Ingredient_Repository
    from service.Extended_USDA_Ingredient_Service import (
        Extended_USDA_Ingredient_Service,
    )
    from dto.Extended_USDA_Ingredient_DTO import Extended_USDA_Ingredient_DTO

    if request.method == "GET":
        extended_usda_ingredient_domains = Extended_USDA_Ingredient_Service(
            usda_ingredient_repository=USDA_Ingredient_Repository(db=db)
        ).get_extended_usda_ingredients()
        usda_ingredient_dtos = [
            Extended_USDA_Ingredient_DTO(extended_usda_ingredient_domain=x)
            for x in extended_usda_ingredient_domains
        ]
        serialized_usda_ingredients = [x.serialize() for x in usda_ingredient_dtos]
        return jsonify(serialized_usda_ingredients), 200
    else:
        return Response(status=405)


@app.route("/api/recipe_ingredient", methods=["POST", "PUT"])
def recipe_ingredient() -> Response:
    from repository.Recipe_Ingredient_Repository import Recipe_Ingredient_Repository
    from service.Recipe_Ingredient_Service import Recipe_Ingredient_Service
    from dto.Recipe_Ingredient_DTO import Recipe_Ingredient_DTO

    if request.method == "POST":
        recipe_ingredients = json.loads(request.data)
        recipe_ingredient_dtos = [
            Recipe_Ingredient_DTO(recipe_ingredient_json=x) for x in recipe_ingredients
        ]
        Recipe_Ingredient_Service(
            recipe_ingredient_repository=Recipe_Ingredient_Repository(db=db)
        ).create_recipe_ingredients(recipe_ingredient_dtos=recipe_ingredient_dtos)
        return Response(status=201)
    elif request.method == "PUT":
        updated_recipe_ingredients = json.loads(request.data)
        updated_recipe_ingredient_DTOs = [
            Recipe_Ingredient_DTO(recipe_ingredient_json=x)
            for x in updated_recipe_ingredients
        ]
        Recipe_Ingredient_Service(
            recipe_ingredient_repository=Recipe_Ingredient_Repository(db=db)
        ).update_recipe_ingredients(
            recipe_ingredient_dtos=updated_recipe_ingredient_DTOs
        )
        return Response(status=204)
    else:
        return Response(status=405)


@app.route("/api/recipe_ingredient_nutrient", methods=["POST", "PUT"])
def recipe_ingredient_nutrient() -> Response:
    from service.Recipe_Ingredient_Service import Recipe_Ingredient_Service
    from service.Recipe_Ingredient_Nutrient_Service import (
        Recipe_Ingredient_Nutrient_Service,
    )
    from service.Meal_Plan_Meal_Service import Meal_Plan_Meal_Service
    from service.Meal_Plan_Snack_Service import Meal_Plan_Snack_Service
    from service.USDA_Ingredient_Service import USDA_Ingredient_Service
    from service.USDA_Ingredient_Portion_Service import USDA_Ingredient_Portion_Service
    from service.USDA_Ingredient_Nutrient_Service import (
        USDA_Ingredient_Nutrient_Service,
    )
    from service.Nutrient_Service import Nutrient_Service
    from service.USDA_Nutrient_Daily_Value_Service import (
        USDA_Nutrient_Daily_Value_Service,
    )
    from repository.Recipe_Ingredient_Repository import Recipe_Ingredient_Repository
    from repository.Recipe_Ingredient_Nutrient_Repository import (
        Recipe_Ingredient_Nutrient_Repository,
    )
    from repository.Meal_Plan_Meal_Repository import Meal_Plan_Meal_Repository
    from repository.Meal_Plan_Snack_Repository import Meal_Plan_Snack_Repository
    from repository.USDA_Ingredient_Repository import USDA_Ingredient_Repository
    from repository.USDA_Ingredient_Portion_Repository import (
        USDA_Ingredient_Portion_Repository,
    )
    from repository.Nutrient_Repository import Nutrient_Repository
    from repository.USDA_Ingredient_Nutrient_Repository import (
        USDA_Ingredient_Nutrient_Repository,
    )
    from repository.USDA_Nutrient_Daily_Value_Repository import (
        USDA_Nutrient_Daily_Value_Repository,
    )
    from dto.Recipe_Ingredient_DTO import Recipe_Ingredient_DTO

    if request.method == "POST":
        recipe_ingredients = json.loads(request.data)
        recipe_ingredient_dtos = [
            Recipe_Ingredient_DTO(recipe_ingredient_json=x) for x in recipe_ingredients
        ]

        Recipe_Ingredient_Nutrient_Service(
            recipe_ingredient_nutrient_repository=Recipe_Ingredient_Nutrient_Repository(
                db=db
            )
        ).create_recipe_ingredient_nutrients(
            recipe_ingredient_dtos=recipe_ingredient_dtos,
            meal_plan_meal_service=Meal_Plan_Meal_Service(
                meal_plan_meal_repository=Meal_Plan_Meal_Repository(db=db)
            ),
            meal_plan_snack_service=Meal_Plan_Snack_Service(
                meal_plan_snack_repository=Meal_Plan_Snack_Repository(db=db)
            ),
            usda_ingredient_service=USDA_Ingredient_Service(
                usda_ingredient_repository=USDA_Ingredient_Repository(db=db)
            ),
            usda_ingredient_portion_service=USDA_Ingredient_Portion_Service(
                usda_ingredient_portion_repository=USDA_Ingredient_Portion_Repository(
                    db=db
                )
            ),
            usda_ingredient_nutrient_service=USDA_Ingredient_Nutrient_Service(
                usda_ingredient_nutrient_repository=USDA_Ingredient_Nutrient_Repository(
                    db=db
                )
            ),
            nutrient_service=Nutrient_Service(
                nutrient_repository=Nutrient_Repository(db=db)
            ),
            usda_nutrient_daily_value_service=USDA_Nutrient_Daily_Value_Service(
                usda_nutrient_daily_value_repository=USDA_Nutrient_Daily_Value_Repository(
                    db=db
                )
            ),
        )
        return Response(status=201)
    elif request.method == "PUT":
        recipe_ingredients = json.loads(request.data)
        recipe_ingredient_dtos = [
            Recipe_Ingredient_DTO(recipe_ingredient_json=x) for x in recipe_ingredients
        ]
        Recipe_Ingredient_Nutrient_Service(
            recipe_ingredient_nutrient_repository=Recipe_Ingredient_Nutrient_Repository(
                db=db
            )
        ).update_recipe_ingredient_nutrients(
            recipe_ingredient_dtos=recipe_ingredient_dtos,
            recipe_ingredient_service=Recipe_Ingredient_Service(
                recipe_ingredient_repository=Recipe_Ingredient_Repository(db=db)
            ),
        )
        return Response(status=201)

    else:
        return Response(status=405)


@app.route("/api/extended_meal", methods=["GET"])
# @requires_auth
def extended_meal() -> Response:
    from service.Extended_Meal_Service import Extended_Meal_Service
    from repository.Meal_Repository import Meal_Repository
    from dto.Extended_Meal_DTO import Extended_Meal_DTO

    if request.method == "GET":
        extended_meal_dtos = [
            Extended_Meal_DTO(extended_meal_domain=x)
            for x in Extended_Meal_Service(
                meal_repository=Meal_Repository(db=db)
            ).get_extended_meals()
        ]
        serialized_extended_meal_dtos = [x.serialize() for x in extended_meal_dtos]
        return jsonify(serialized_extended_meal_dtos), 200
    else:
        return Response(status=405)


@app.route("/api/meal_dietary_restriction", methods=["POST"])
def meal_dietary_restriction() -> Response:
    from service.Meal_Dietary_Restriction_Service import (
        Meal_Dietary_Restriction_Service,
    )
    from repository.Meal_Dietary_Restriction_Repository import (
        Meal_Dietary_Restriction_Repository,
    )
    from dto.Meal_Dietary_Restriction_DTO import Meal_Dietary_Restriction_DTO

    if request.method == "POST":
        new_meal_dietary_restriction = Meal_Dietary_Restriction_DTO(
            meal_dietary_restriction_json=json.loads(request.data)
        )
        Meal_Dietary_Restriction_Service(
            meal_dietary_restriction_repository=Meal_Dietary_Restriction_Repository(
                db=db
            )
        ).create_meal_dietary_restriction(
            meal_dietary_restriction_dto=new_meal_dietary_restriction
        )
        return Response(status=201)

    else:
        return Response(status=405)


@app.route("/api/dietary_restriction", methods=["GET"])
def dietary_restrictions() -> Response:
    from service.Dietary_Restriction_Service import Dietary_Restriction_Service
    from repository.Dietary_Restriction_Repository import Dietary_Restriction_Repository
    from dto.Dietary_Restriction_DTO import Dietary_Restriction_DTO

    if request.method == "GET":
        dietary_restriction_domains = Dietary_Restriction_Service(
            dietary_restriction_repository=Dietary_Restriction_Repository(db=db)
        ).get_dietary_restrictions()
        dietary_restriction_DTOs = [
            Dietary_Restriction_DTO(dietary_restriction_domain=x)
            for x in dietary_restriction_domains
        ]
        return jsonify([x.serialize() for x in dietary_restriction_DTOs]), 200

    else:
        return Response(status=405)


@app.route("/api/meal/<string:meal_id>", methods=["DELETE"])
@app.route("/api/meal", defaults={"meal_id": None}, methods=["GET", "POST"])
def meal(meal_id: Optional[str]) -> Response:
    from repository.Meal_Repository import Meal_Repository
    from service.Meal_Service import Meal_Service
    from dto.Meal_DTO import Meal_DTO

    if request.method == "GET":
        meals = [
            x.serialize()
            for x in Meal_Service(meal_repository=Meal_Repository(db=db)).get_meals()
        ]
        return jsonify(meals), 200
    elif request.method == "POST":
        meal = json.loads(request.data)
        meal_dto = Meal_DTO(meal_json=meal)
        Meal_Service(meal_repository=Meal_Repository(db=db)).create_meal(
            meal_dto=meal_dto
        )
        return Response(status=201)
    elif request.method == "DELETE":
        from helpers.db.wipe_meal_data import wipe_meal_data

        meal_uuid = UUID(meal_id)
        wipe_meal_data(db=db, meal_id=meal_uuid)
        return Response(status=200, response="Wiped meal data")
    else:
        return Response(status=405)


@app.route("/api/meal_plan_meal", methods=["POST", "PUT"])
def meal_plan_meal() -> Response:
    from service.Meal_Plan_Meal_Service import Meal_Plan_Meal_Service
    from repository.Meal_Plan_Meal_Repository import Meal_Plan_Meal_Repository
    from dto.Meal_Plan_Meal_DTO import Meal_Plan_Meal_DTO

    if request.method == "POST":
        meal_plan_meal_data = json.loads(request.data)
        meal_plan_meal_dto = Meal_Plan_Meal_DTO(meal_plan_meal_json=meal_plan_meal_data)
        Meal_Plan_Meal_Service(
            meal_plan_meal_repository=Meal_Plan_Meal_Repository(db=db)
        ).create_meal_plan_meal(meal_plan_meal_dto=meal_plan_meal_dto)
        return Response(status=201)
    elif request.method == "PUT":
        meal_plan_meal = json.loads(request.data)
        meal_plan_meal_dto = Meal_Plan_Meal_DTO(meal_plan_meal_json=meal_plan_meal)

        Meal_Plan_Meal_Service(
            meal_plan_meal_repository=Meal_Plan_Meal_Repository(db=db)
        ).update_meal_plan_meal(meal_plan_meal_dto=meal_plan_meal_dto),

        return Response(status=204)
    else:
        return Response(status=405)


@app.route("/api/extended_meal_plan_meal", methods=["GET", "PUT"])
def extended_meal_plan_meal() -> Response:
    from repository.Meal_Plan_Meal_Repository import Meal_Plan_Meal_Repository
    from repository.Meal_Plan_Repository import Meal_Plan_Repository
    from service.Extended_Meal_Plan_Meal_Service import Extended_Meal_Plan_Meal_Service
    from service.Meal_Plan_Service import Meal_Plan_Service
    from domain.Extended_Meal_Plan_Meal_Domain import Extended_Meal_Plan_Meal_Domain
    from dto.Extended_Meal_Plan_Meal_DTO import Extended_Meal_Plan_Meal_DTO
    from dto.Recipe_Ingredient_DTO import Recipe_Ingredient_DTO

    if request.method == "GET":
        meal_plan_id = request.args.get("meal_plan_id")
        meal_id = request.args.get("meal_id")
        meal_plan_number = request.args.get("meal_plan_number")
        if not meal_id:
            if meal_plan_number:
                associated_meal_plan = Meal_Plan_Service(
                    meal_plan_repository=Meal_Plan_Repository(db=db)
                ).get_meal_plan(meal_plan_number=meal_plan_number)
                extended_meal_plan_meals = Extended_Meal_Plan_Meal_Service(
                    meal_plan_meal_repository=Meal_Plan_Meal_Repository(db=db)
                ).get_specific_extended_meal_plan_meals(
                    meal_plan_id=associated_meal_plan.id
                )
                if extended_meal_plan_meals:
                    meal_plan_meal_DTOs = [
                        Extended_Meal_Plan_Meal_DTO(extended_meal_plan_meal_domain=x)
                        for x in extended_meal_plan_meals
                    ]
                    serialized_meal_plan_meal_DTOs = [
                        x.serialize() for x in meal_plan_meal_DTOs
                    ]
                else:
                    return Response(status=404)
            elif not meal_plan_id and not meal_id:
                extended_meal_plan_meals: Optional[
                    list[Extended_Meal_Plan_Meal_Domain]
                ] = Extended_Meal_Plan_Meal_Service(
                    meal_plan_meal_repository=Meal_Plan_Meal_Repository(db=db)
                ).get_extended_meal_plan_meals()
                if extended_meal_plan_meals:
                    meal_plan_meal_DTOs = [
                        Extended_Meal_Plan_Meal_DTO(extended_meal_plan_meal_domain=x)
                        for x in extended_meal_plan_meals
                    ]
                    serialized_meal_plan_meal_DTOs = [
                        x.serialize() for x in meal_plan_meal_DTOs
                    ]
                else:
                    return Response(status=404)
            elif meal_plan_id and not meal_id:
                extended_meal_plan_meals = Extended_Meal_Plan_Meal_Service(
                    meal_plan_meal_repository=Meal_Plan_Meal_Repository(db=db)
                ).get_specific_extended_meal_plan_meals(meal_plan_id=meal_plan_id)
                if extended_meal_plan_meals:
                    meal_plan_meal_DTOs = [
                        Extended_Meal_Plan_Meal_DTO(extended_meal_plan_meal_domain=x)
                        for x in extended_meal_plan_meals
                    ]
                    serialized_meal_plan_meal_DTOs = [
                        x.serialize() for x in meal_plan_meal_DTOs
                    ]
                else:
                    return Response(status=404)
            return jsonify(serialized_meal_plan_meal_DTOs), 200
        else:
            extended_meal_plan_meal = Extended_Meal_Plan_Meal_Service(
                meal_plan_meal_repository=Meal_Plan_Meal_Repository(db=db)
            ).get_extended_meal_plan_meal(
                meal_plan_meal_id=None, meal_plan_id=meal_plan_id, meal_id=meal_id
            )
            if extended_meal_plan_meal:
                meal_plan_meal_DTO = Extended_Meal_Plan_Meal_DTO(
                    extended_meal_plan_meal_domain=extended_meal_plan_meal
                )

                serialized_meal_plan_meal_DTO = meal_plan_meal_DTO.serialize()
                return jsonify(serialized_meal_plan_meal_DTO), 200
            else:
                return jsonify([]), 200
    elif request.method == "PUT":
        ephemeral_meal_plan_meal = json.loads(request.data)
        # Get new quantity values for recipe ingredients to compute changes to nutrient amounts
        updated_recipe = ephemeral_meal_plan_meal["recipe"]
        updated_recipe_dtos = [
            Recipe_Ingredient_DTO(recipe_ingredient_json=x) for x in updated_recipe
        ]
        updated_meal_plan_meal = Extended_Meal_Plan_Meal_Service(
            meal_plan_meal_repository=Meal_Plan_Meal_Repository(db=db)
        ).compute_new_meal_plan_meal(
            meal_plan_meal_id=ephemeral_meal_plan_meal["id"],
            updated_recipe=updated_recipe_dtos,
        )

        updated_meal_plan_meal_dto = Extended_Meal_Plan_Meal_DTO(
            extended_meal_plan_meal_domain=updated_meal_plan_meal
        )
        return jsonify(updated_meal_plan_meal_dto.serialize()), 200
    else:
        return Response(status=405)


@app.route("/api/extended_scheduled_order_meal", methods=["GET"])
def extended_scheduled_order_meal() -> Response:
    from service.Extended_Scheduled_Order_Meal_Service import (
        Extended_Scheduled_Order_Meal_Service,
    )
    from repository.Scheduled_Order_Meal_Repository import (
        Scheduled_Order_Meal_Repository,
    )
    from domain.Extended_Scheduled_Order_Meal_Domain import (
        Extended_Scheduled_Order_Meal_Domain,
    )
    from dto.Extended_Scheduled_Order_Meal_DTO import Extended_Scheduled_Order_Meal_DTO

    meal_subscription_id: str = request.args.get("meal_subscription_id")
    if request.method == "GET":
        extended_scheduled_order_meal_domains: Optional[
            list[Extended_Scheduled_Order_Meal_Domain]
        ] = Extended_Scheduled_Order_Meal_Service(
            scheduled_order_meal_repository=Scheduled_Order_Meal_Repository(db=db)
        ).get_upcoming_extended_scheduled_order_meals(
            meal_subscription_id=meal_subscription_id
        )
        if extended_scheduled_order_meal_domains:
            extended_scheduled_order_meal_dtos: list[
                Extended_Scheduled_Order_Meal_DTO
            ] = [
                Extended_Scheduled_Order_Meal_DTO(
                    extended_scheduled_order_meal_domain=x
                )
                for x in extended_scheduled_order_meal_domains
            ]
            serialized_extended_scheduled_order_meal_dtos: list[dict] = [
                x.serialize() for x in extended_scheduled_order_meal_dtos
            ]
            return jsonify(serialized_extended_scheduled_order_meal_dtos), 200
        else:
            return Response(status=204)
    else:
        return Response(status=405)


@app.route("/api/scheduled_order_meal", methods=["GET", "POST", "PUT", "DELETE"])
def scheduled_order_meal() -> Response:
    from service.Date_Service import Date_Service
    from service.Scheduled_Order_Meal_Service import Scheduled_Order_Meal_Service
    from repository.Scheduled_Order_Meal_Repository import (
        Scheduled_Order_Meal_Repository,
    )
    from domain.Scheduled_Order_Meal_Domain import Scheduled_Order_Meal_Domain
    from dto.Scheduled_Order_Meal_DTO import Scheduled_Order_Meal_DTO

    if request.method == "POST":
        scheduled_order_meals_json: list[dict] = json.loads(request.data)
        scheduled_order_meal_dtos = [
            Scheduled_Order_Meal_DTO(scheduled_order_meal_json=x)
            for x in scheduled_order_meals_json
        ]
        Scheduled_Order_Meal_Service(
            scheduled_order_meal_repository=Scheduled_Order_Meal_Repository(db=db)
        ).create_scheduled_order_meals(
            scheduled_order_meal_dtos=scheduled_order_meal_dtos
        )
        return Response(status=201)
    elif request.method == "GET":
        meal_subscription_id: str = request.args.get("meal_subscription_id")
        scheduled_order_meal_domains: Optional[
            list[Scheduled_Order_Meal_Domain]
        ] = Scheduled_Order_Meal_Service(
            scheduled_order_meal_repository=Scheduled_Order_Meal_Repository(db=db)
        ).get_scheduled_order_meals(
            meal_subscription_id=meal_subscription_id
        )
        if scheduled_order_meal_domains:
            scheduled_order_meal_dtos = [
                Scheduled_Order_Meal_DTO(scheduled_order_meal_domain=x)
                for x in scheduled_order_meal_domains
            ]
            serialized_scheduled_order_meal_dtos: list[dict] = [
                x.serialize() for x in scheduled_order_meal_dtos
            ]
            return jsonify(serialized_scheduled_order_meal_dtos), 200
        else:
            return Response(status=404)
    elif request.method == "PUT":
        meal_subscription_id: Optional[str] = request.args.get("meal_subscription_id")
        if not meal_subscription_id:
            # Handle changes to scheduled order meals on home page
            scheduled_order_meals_json = json.loads(request.data)
            scheduled_order_meal_dtos = [
                Scheduled_Order_Meal_DTO(scheduled_order_meal_json=x)
                for x in scheduled_order_meals_json
            ]
            Scheduled_Order_Meal_Service(
                scheduled_order_meal_repository=Scheduled_Order_Meal_Repository(db=db)
            ).update_home_page_scheduled_order_meals(
                scheduled_order_meal_dtos=scheduled_order_meal_dtos
            )
        else:
            should_pause_scheduled_order_meals: bool = (
                request.headers.get("update") == "pause"
            )
            if should_pause_scheduled_order_meals:
                Scheduled_Order_Meal_Service(
                    scheduled_order_meal_repository=Scheduled_Order_Meal_Repository(
                        db=db
                    )
                ).pause_scheduled_order_meals(meal_subscription_id=meal_subscription_id)
            else:
                Scheduled_Order_Meal_Service(
                    scheduled_order_meal_repository=Scheduled_Order_Meal_Repository(
                        db=db
                    )
                ).unpause_scheduled_order_meals(
                    meal_subscription_id=meal_subscription_id
                )
        return Response(status=204)
    elif request.method == "DELETE":
        meal_subscription_id: str = request.args.get("meal_subscription_id")
        # Check if past cutoff date and if it is the client's first week of meals
        cutoff_date = Date_Service().get_current_week_cutoff(
            Date_Service().get_current_week_delivery_date()
        )
        is_first_week = Scheduled_Order_Meal_Service(
            scheduled_order_meal_repository=Scheduled_Order_Meal_Repository(db=db)
        ).check_if_first_week_of_meals(meal_subscription_id=meal_subscription_id)
        Scheduled_Order_Meal_Service(
            scheduled_order_meal_repository=Scheduled_Order_Meal_Repository(db=db)
        ).delete_scheduled_order_meals(
            meal_subscription_id=meal_subscription_id,
            cutoff_date=cutoff_date,
            current_week_delivery_date=Date_Service().get_current_week_delivery_date(),
            is_first_week=is_first_week,
        )
        return Response(status=204)
    else:
        return Response(status=405)


@app.route("/api/extended_schedule_meal", methods=["GET"])
# @requires_auth
def extended_schedule_meal() -> Response:
    from service.Extended_Schedule_Meal_Service import Extended_Schedule_Meal_Service
    from service.Client_Service import Client_Service
    from repository.Schedule_Meal_Repository import Schedule_Meal_Repository
    from repository.Client_Repository import Client_Repository
    from domain.Extended_Schedule_Meal_Domain import Extended_Schedule_Meal_Domain
    from dto.Extended_Schedule_Meal_DTO import Extended_Schedule_Meal_DTO

    if request.method == "GET":
        meal_subscription_id: str | None = request.args.get("meal_subscription_id")

        if meal_subscription_id:
            extended_schedule_meal_domains = Extended_Schedule_Meal_Service(
                schedule_meal_repository=Schedule_Meal_Repository(db=db)
            ).get_extended_schedule_meals(meal_subscription_id=meal_subscription_id)
            extended_schedule_meal_DTOs = [
                Extended_Schedule_Meal_DTO(extended_schedule_meal_domain=x)
                for x in extended_schedule_meal_domains
            ]
            serialized_extended_schedule_meals: list[dict] = [
                x.serialize() for x in extended_schedule_meal_DTOs
            ]
            return jsonify(serialized_extended_schedule_meals), 200

        else:
            dietitian_id = request.args.get("dietitian_id")
            extended_schedule_meal_domains: list[
                Optional[Extended_Schedule_Meal_Domain]
            ] = Extended_Schedule_Meal_Service(
                schedule_meal_repository=Schedule_Meal_Repository(db=db)
            ).get_dietitian_extended_schedule_meals(
                dietitian_id=dietitian_id,
                client_service=Client_Service(
                    client_repository=Client_Repository(db=db)
                ),
            )
            if extended_schedule_meal_domains:
                extended_schedule_meal_DTOs = [
                    Extended_Schedule_Meal_DTO(extended_schedule_meal_domain=x)
                    for x in extended_schedule_meal_domains
                ]
                serialized_extended_schedule_meals: list[dict] = [
                    x.serialize() for x in extended_schedule_meal_DTOs
                ]
                return jsonify(serialized_extended_schedule_meals), 200
            else:
                return Response(status=204)

    else:
        return Response(status=405)


@app.route("/api/schedule_meal", methods=["GET", "POST", "DELETE"])
def schedule_meal() -> Response:
    from service.Schedule_Meal_Service import Schedule_Meal_Service
    from service.Client_Service import Client_Service
    from repository.Schedule_Meal_Repository import Schedule_Meal_Repository
    from repository.Client_Repository import Client_Repository
    from domain.Schedule_Meal_Domain import Schedule_Meal_Domain
    from dto.Schedule_Meal_DTO import Schedule_Meal_DTO

    if request.method == "POST":
        schedule_meals_JSON = json.loads(request.data)
        schedule_meal_DTOs = [
            Schedule_Meal_DTO(schedule_meal_json=x) for x in schedule_meals_JSON
        ]
        Schedule_Meal_Service(
            schedule_meal_repository=Schedule_Meal_Repository(db=db)
        ).create_schedule_meals(schedule_meal_dtos=schedule_meal_DTOs)
        return Response(status=201)

    elif request.method == "GET":
        meal_subscription_id: str | None = request.args.get("meal_subscription_id")

        if meal_subscription_id:
            schedule_meal_domains: list[Schedule_Meal_Domain] = Schedule_Meal_Service(
                schedule_meal_repository=Schedule_Meal_Repository(db=db)
            ).get_schedule_meals(meal_subscription_id=meal_subscription_id)
            schedule_meal_DTOs = [
                Schedule_Meal_DTO(schedule_meal_domain=x) for x in schedule_meal_domains
            ]
            serialized_schedule_meals: list[dict] = [
                x.serialize() for x in schedule_meal_DTOs
            ]
            return jsonify(serialized_schedule_meals), 200

        else:
            dietitian_id: str | None = request.args.get("dietitian_id")
            schedule_meal_domains: list[Schedule_Meal_Domain] = Schedule_Meal_Service(
                schedule_meal_repository=Schedule_Meal_Repository(db=db)
            ).get_dietitian_schedule_meals(
                dietitian_id=dietitian_id,
                client_service=Client_Service(
                    client_repository=Client_Repository(db=db)
                ),
            )
            schedule_meal_DTOs = [
                Schedule_Meal_DTO(schedule_meal_domain=x) for x in schedule_meal_domains
            ]
            serialized_schedule_meals: list[dict] = [
                x.serialize() for x in schedule_meal_DTOs
            ]
            return jsonify(serialized_schedule_meals), 200

    elif request.method == "DELETE":
        meal_subscription_id = request.args.get("meal_subscription_id")
        Schedule_Meal_Service(
            schedule_meal_repository=Schedule_Meal_Repository(db=db)
        ).delete_schedule_meals(meal_subscription_id=meal_subscription_id)
        return Response(status=204)

    else:
        return Response(status=405)


@app.route("/api/extended_staged_schedule_meal", methods=["GET"])
def extended_staged_schedule_meal() -> Response:
    from service.Extended_Staged_Schedule_Meal_Service import (
        Extended_Staged_Schedule_Meal_Service,
    )
    from repository.Staged_Schedule_Meal_Repository import (
        Staged_Schedule_Meal_Repository,
    )
    from domain.Extended_Staged_Schedule_Meal_Domain import (
        Extended_Staged_Schedule_Meal_Domain,
    )
    from dto.Extended_Staged_Schedule_Meal_DTO import Extended_Staged_Schedule_Meal_DTO

    if request.method == "GET":
        staged_client_id: str = request.args.get("staged_client_id")
        extended_staged_schedule_meal_domains: Optional[
            list[Extended_Staged_Schedule_Meal_Domain]
        ] = Extended_Staged_Schedule_Meal_Service(
            staged_schedule_meal_repository=Staged_Schedule_Meal_Repository(db=db)
        ).get_staged_schedule_meals(
            staged_client_id=staged_client_id
        )
        if extended_staged_schedule_meal_domains:
            staged_schedule_meal_dtos = [
                Extended_Staged_Schedule_Meal_DTO(
                    extended_staged_schedule_meal_domain=x
                )
                for x in extended_staged_schedule_meal_domains
            ]
            serialized_staged_schedule_meal_DTOs = [
                x.serialize() for x in staged_schedule_meal_dtos
            ]
        return jsonify(serialized_staged_schedule_meal_DTOs), 200
    else:
        return Response(status=405)


@app.route("/api/staged_schedule_meal", methods=["GET", "POST"])
def staged_schedule_meal() -> Response:
    from repository.Staged_Schedule_Meal_Repository import (
        Staged_Schedule_Meal_Repository,
    )
    from service.Staged_Schedule_Meal_Service import Staged_Schedule_Meal_Service
    from dto.Staged_Schedule_Meal_DTO import Staged_Schedule_Meal_DTO

    if request.method == "POST":
        staged_schedule_meals_JSON = json.loads(request.data)
        staged_schedule_meal_DTOs = [
            Staged_Schedule_Meal_DTO(staged_schedule_meal_json=x)
            for x in staged_schedule_meals_JSON
        ]
        Staged_Schedule_Meal_Service(
            staged_schedule_meal_repository=Staged_Schedule_Meal_Repository(db=db)
        ).create_staged_schedule_meals(
            staged_schedule_meal_dtos=staged_schedule_meal_DTOs
        )
        return Response(status=201)

    elif request.method == "GET":
        staged_client_id = request.args.get("staged_client_id")
        staged_schedule_meal_doamins = Staged_Schedule_Meal_Service(
            staged_schedule_meal_repository=Staged_Schedule_Meal_Repository(db=db)
        ).get_staged_schedule_meals(staged_client_id=staged_client_id)
        staged_schedule_meal_DTOs = [
            Staged_Schedule_Meal_DTO(staged_schedule_meal_domain=x)
            for x in staged_schedule_meal_doamins
        ]
        return jsonify([x.serialize() for x in staged_schedule_meal_DTOs]), 200
    else:
        return Response(status=405)


# ---> Snacks <--- #
@app.route("/api/snack/<string:snack_id>", methods=["DELETE"])
@app.route("/api/snack", defaults={"snack_id": None}, methods=["GET", "POST"])
# @requires_auth
def snack(snack_id: Optional[str]) -> Response:
    from repository.Snack_Repository import Snack_Repository
    from service.Snack_Service import Snack_Service
    from dto.Snack_DTO import Snack_DTO

    if request.method == "GET":
        snacks = [
            x.serialize()
            for x in Snack_Service(
                snack_repository=Snack_Repository(db=db)
            ).get_snacks()
        ]
        return jsonify(snacks), 200
    elif request.method == "POST":
        snack = json.loads(request.data)
        snack_dto = Snack_DTO(snack_json=snack)
        Snack_Service(snack_repository=Snack_Repository(db=db)).create_snack(
            snack_dto=snack_dto
        )
        return Response(status=201)
    elif request.method == "DELETE":
        from helpers.db.wipe_snack_data import wipe_snack_data

        snack_uuid = UUID(snack_id)
        wipe_snack_data(db=db, snack_id=snack_uuid)
        return Response(status=200, response="Wiped snack data")
    else:
        return Response(status=405)


@app.route("/api/schedule_snack", methods=["GET", "POST", "DELETE"])
def schedule_snack() -> Response:
    from service.Schedule_Snack_Service import Schedule_Snack_Service
    from service.Client_Service import Client_Service
    from repository.Schedule_Snack_Repository import Schedule_Snack_Repository
    from repository.Client_Repository import Client_Repository
    from domain.Schedule_Snack_Domain import Schedule_Snack_Domain
    from dto.Schedule_Snack_DTO import Schedule_Snack_DTO

    if request.method == "POST":
        schedule_snacks_JSON = json.loads(request.data)
        schedule_snack_DTOs = [
            Schedule_Snack_DTO(schedule_snack_json=x) for x in schedule_snacks_JSON
        ]
        Schedule_Snack_Service(
            schedule_snack_repository=Schedule_Snack_Repository(db=db)
        ).create_schedule_snacks(schedule_snack_dtos=schedule_snack_DTOs)
        return Response(status=201)

    elif request.method == "GET":
        meal_subscription_id: str | None = request.args.get("meal_subscription_id")

        if meal_subscription_id:
            schedule_snack_domains: list[
                Schedule_Snack_Domain
            ] = Schedule_Snack_Service(
                schedule_snack_repository=Schedule_Snack_Repository(db=db)
            ).get_schedule_snacks(
                meal_subscription_id=meal_subscription_id
            )
            schedule_snack_DTOs = [
                Schedule_Snack_DTO(schedule_snack_domain=x)
                for x in schedule_snack_domains
            ]
            serialized_schedule_snacks: list[dict] = [
                x.serialize() for x in schedule_snack_DTOs
            ]
            return jsonify(serialized_schedule_snacks), 200

        else:
            dietitian_id: str | None = request.args.get("dietitian_id")
            schedule_snack_domains: list[
                Schedule_Snack_Domain
            ] = Schedule_Snack_Service(
                schedule_snack_repository=Schedule_Snack_Repository(db=db)
            ).get_dietitian_schedule_snacks(
                dietitian_id=dietitian_id,
                client_service=Client_Service(
                    client_repository=Client_Repository(db=db)
                ),
            )
            schedule_snack_DTOs = [
                Schedule_Snack_DTO(schedule_snack_domain=x)
                for x in schedule_snack_domains
            ]
            serialized_schedule_snacks: list[dict] = [
                x.serialize() for x in schedule_snack_DTOs
            ]
            return jsonify(serialized_schedule_snacks), 200

    elif request.method == "DELETE":
        meal_subscription_id = request.args.get("meal_subscription_id")
        Schedule_Snack_Service(
            schedule_snack_repository=Schedule_Snack_Repository(db=db)
        ).delete_schedule_snacks(meal_subscription_id=meal_subscription_id)
        return Response(status=204)

    else:
        return Response(status=405)


@app.route("/api/scheduled_order_snack", methods=["GET", "POST", "PUT", "DELETE"])
def scheduled_order_snack() -> Response:
    from service.Date_Service import Date_Service
    from service.Scheduled_Order_Snack_Service import Scheduled_Order_Snack_Service
    from repository.Scheduled_Order_Snack_Repository import (
        Scheduled_Order_Snack_Repository,
    )
    from domain.Scheduled_Order_Snack_Domain import Scheduled_Order_Snack_Domain
    from dto.Scheduled_Order_Snack_DTO import Scheduled_Order_Snack_DTO

    if request.method == "POST":
        scheduled_order_snacks_json: list[dict] = json.loads(request.data)
        scheduled_order_snack_dtos = [
            Scheduled_Order_Snack_DTO(scheduled_order_snack_json=x)
            for x in scheduled_order_snacks_json
        ]
        Scheduled_Order_Snack_Service(
            scheduled_order_snack_repository=Scheduled_Order_Snack_Repository(db=db)
        ).create_scheduled_order_snacks(
            scheduled_order_snack_dtos=scheduled_order_snack_dtos
        )
        return Response(status=201)
    elif request.method == "GET":
        meal_subscription_id: str = request.args.get("meal_subscription_id")
        scheduled_order_snack_domains: Optional[
            list[Scheduled_Order_Snack_Domain]
        ] = Scheduled_Order_Snack_Service(
            scheduled_order_snack_repository=Scheduled_Order_Snack_Repository(db=db)
        ).get_scheduled_order_snacks(
            meal_subscription_id=meal_subscription_id
        )
        if scheduled_order_snack_domains:
            scheduled_order_snack_dtos = [
                Scheduled_Order_Snack_DTO(scheduled_order_snack_domain=x)
                for x in scheduled_order_snack_domains
            ]
            serialized_scheduled_order_snack_dtos: list[dict] = [
                x.serialize() for x in scheduled_order_snack_dtos
            ]
            return jsonify(serialized_scheduled_order_snack_dtos), 200
        else:
            return Response(status=404)
    elif request.method == "PUT":
        meal_subscription_id: Optional[str] = request.args.get("meal_subscription_id")
        if not meal_subscription_id:
            # Handle changes to scheduled order snacks on home page
            scheduled_order_snacks_json = json.loads(request.data)
            scheduled_order_snack_dtos = [
                Scheduled_Order_Snack_DTO(scheduled_order_snack_json=x)
                for x in scheduled_order_snacks_json
            ]
            Scheduled_Order_Snack_Service(
                scheduled_order_snack_repository=Scheduled_Order_Snack_Repository(db=db)
            ).update_home_page_scheduled_order_snacks(
                scheduled_order_snack_dtos=scheduled_order_snack_dtos
            )
        else:
            should_pause_scheduled_order_snacks: bool = (
                request.headers.get("update") == "pause"
            )
            if should_pause_scheduled_order_snacks:
                Scheduled_Order_Snack_Service(
                    scheduled_order_snack_repository=Scheduled_Order_Snack_Repository(
                        db=db
                    )
                ).pause_scheduled_order_snacks(
                    meal_subscription_id=meal_subscription_id
                )
            else:
                Scheduled_Order_Snack_Service(
                    scheduled_order_snack_repository=Scheduled_Order_Snack_Repository(
                        db=db
                    )
                ).unpause_scheduled_order_snacks(
                    meal_subscription_id=meal_subscription_id
                )
        return Response(status=204)
    elif request.method == "DELETE":
        meal_subscription_id: str = request.args.get("meal_subscription_id")
        # Check if past cutoff date and if it is the client's first week of snacks
        cutoff_date = Date_Service().get_current_week_cutoff(
            Date_Service().get_current_week_delivery_date()
        )
        is_first_week = Scheduled_Order_Snack_Service(
            scheduled_order_snack_repository=Scheduled_Order_Snack_Repository(db=db)
        ).check_if_first_week_of_snacks(meal_subscription_id=meal_subscription_id)

        Scheduled_Order_Snack_Service(
            scheduled_order_snack_repository=Scheduled_Order_Snack_Repository(db=db)
        ).delete_scheduled_order_snacks(
            meal_subscription_id=meal_subscription_id,
            cutoff_date=cutoff_date,
            current_week_delivery_date=Date_Service().get_current_week_delivery_date(),
            is_first_week=is_first_week,
        )
        return Response(status=204)
    else:
        return Response(status=405)


@app.route("/api/extended_scheduled_order_snack", methods=["GET"])
def extended_scheduled_order_snack() -> Response:
    from service.Extended_Scheduled_Order_Snack_Service import (
        Extended_Scheduled_Order_Snack_Service,
    )
    from repository.Scheduled_Order_Snack_Repository import (
        Scheduled_Order_Snack_Repository,
    )
    from domain.Extended_Scheduled_Order_Snack_Domain import (
        Extended_Scheduled_Order_Snack_Domain,
    )
    from dto.Extended_Scheduled_Order_Snack_DTO import (
        Extended_Scheduled_Order_Snack_DTO,
    )

    meal_subscription_id: str = request.args.get("meal_subscription_id")
    if request.method == "GET":
        extended_scheduled_order_snack_domains: Optional[
            list[Extended_Scheduled_Order_Snack_Domain]
        ] = Extended_Scheduled_Order_Snack_Service(
            scheduled_order_snack_repository=Scheduled_Order_Snack_Repository(db=db)
        ).get_upcoming_extended_scheduled_order_snacks(
            meal_subscription_id=meal_subscription_id
        )
        if extended_scheduled_order_snack_domains:
            extended_scheduled_order_snack_dtos: list[
                Extended_Scheduled_Order_Snack_DTO
            ] = [
                Extended_Scheduled_Order_Snack_DTO(
                    extended_scheduled_order_snack_domain=x
                )
                for x in extended_scheduled_order_snack_domains
            ]
            serialized_extended_scheduled_order_snack_dtos: list[dict] = [
                x.serialize() for x in extended_scheduled_order_snack_dtos
            ]
            return jsonify(serialized_extended_scheduled_order_snack_dtos), 200
        else:
            return Response(status=204)
    else:
        return Response(status=405)


@app.route("/api/order_snack", methods=["POST", "GET"])
def order_snack() -> Response:
    from service.Order_Snack_Service import Order_Snack_Service
    from repository.Order_Snack_Repository import Order_Snack_Repository
    from domain.Order_Snack_Domain import Order_Snack_Domain
    from dto.Order_Snack_DTO import Order_Snack_DTO

    if request.method == "POST":
        order_snacks_json = json.loads(request.data)
        order_snack_DTOs = [
            Order_Snack_DTO(order_snack_json=x) for x in order_snacks_json
        ]
        Order_Snack_Service(
            order_snack_repository=Order_Snack_Repository(db=db)
        ).create_order_snacks(order_snack_dtos=order_snack_DTOs)
        return Response(status=201)
    elif request.method == "GET":
        meal_subscription_id: str = request.args.get("meal_subscription_id")
        order_snack_domains: Optional[list[Order_Snack_Domain]] = Order_Snack_Service(
            order_snack_repository=Order_Snack_Repository(db=db)
        ).get_order_snacks(meal_subscription_id=meal_subscription_id)
        if order_snack_domains:
            order_snack_DTOs = [
                Order_Snack_DTO(order_snack_domain=x) for x in order_snack_domains
            ]
            serialized_order_snack_DTOs = [x.serialize() for x in order_snack_DTOs]

            return jsonify(serialized_order_snack_DTOs), 200
        else:
            return Response(status=204)
    else:
        return Response(status=405)


@app.route("/api/meal_plan_snack", methods=["PUT", "POST"])
def meal_plan_snack() -> Response:
    from service.Meal_Plan_Snack_Service import Meal_Plan_Snack_Service
    from repository.Meal_Plan_Snack_Repository import Meal_Plan_Snack_Repository
    from dto.Meal_Plan_Snack_DTO import Meal_Plan_Snack_DTO

    if request.method == "GET":
        pass
    if request.method == "PUT":
        meal_plan_snack = json.loads(request.data)
        meal_plan_snack_dto = Meal_Plan_Snack_DTO(meal_plan_snack_json=meal_plan_snack)
        Meal_Plan_Snack_Service(
            meal_plan_snack_repository=Meal_Plan_Snack_Repository(db=db)
        ).update_meal_plan_snack(
            meal_plan_snack_dto=meal_plan_snack_dto,
        )
        return Response(status=204)
    elif request.method == "POST":
        meal_plan_snack_data = json.loads(request.data)
        meal_plan_snack_dto = Meal_Plan_Snack_DTO(
            meal_plan_snack_json=meal_plan_snack_data
        )
        Meal_Plan_Snack_Service(
            meal_plan_snack_repository=Meal_Plan_Snack_Repository(db=db)
        ).create_meal_plan_snack(meal_plan_snack_dto=meal_plan_snack_dto)
        return Response(status=201)
    else:
        return Response(status=405)


@app.route("/api/extended_meal_plan_snack", methods=["GET", "PUT"])
def extended_meal_plan_snack() -> Response:
    from repository.Meal_Plan_Snack_Repository import Meal_Plan_Snack_Repository
    from repository.Meal_Plan_Repository import Meal_Plan_Repository
    from service.Extended_Meal_Plan_Snack_Service import (
        Extended_Meal_Plan_Snack_Service,
    )
    from service.Meal_Plan_Service import Meal_Plan_Service
    from domain.Extended_Meal_Plan_Snack_Domain import Extended_Meal_Plan_Snack_Domain
    from dto.Extended_Meal_Plan_Snack_DTO import Extended_Meal_Plan_Snack_DTO
    from dto.Recipe_Ingredient_DTO import Recipe_Ingredient_DTO

    if request.method == "GET":
        meal_plan_id = request.args.get("meal_plan_id")
        snack_id = request.args.get("snack_id")
        meal_plan_number = request.args.get("meal_plan_number")
        if meal_plan_number:
            associated_meal_plan = Meal_Plan_Service(
                meal_plan_repository=Meal_Plan_Repository(db=db)
            ).get_meal_plan(meal_plan_number=meal_plan_number)
            extended_meal_plan_snack_domains: Optional[
                list[Extended_Meal_Plan_Snack_Domain]
            ] = Extended_Meal_Plan_Snack_Service(
                meal_plan_snack_repository=Meal_Plan_Snack_Repository(db=db)
            ).get_specific_extended_meal_plan_snacks(
                meal_plan_id=associated_meal_plan.id
            )
            if extended_meal_plan_snack_domains:
                extended_meal_plan_snack_dtos = [
                    Extended_Meal_Plan_Snack_DTO(
                        extended_meal_plan_snack_domain=x
                    ).serialize()
                    for x in extended_meal_plan_snack_domains
                ]
                return jsonify(extended_meal_plan_snack_dtos), 200
            else:
                return Response(status=204)
        if not meal_plan_id and not snack_id:
            extended_meal_plan_snacks: Optional[
                list[Extended_Meal_Plan_Snack_Domain]
            ] = Extended_Meal_Plan_Snack_Service(
                meal_plan_snack_repository=Meal_Plan_Snack_Repository(db=db)
            ).get_extended_meal_plan_snacks()
            if extended_meal_plan_snacks:
                meal_plan_snack_DTOs = [
                    Extended_Meal_Plan_Snack_DTO(extended_meal_plan_snack_domain=x)
                    for x in extended_meal_plan_snacks
                ]
                serialized_meal_plan_snack_DTOs = [
                    x.serialize() for x in meal_plan_snack_DTOs
                ]
                return jsonify(serialized_meal_plan_snack_DTOs), 200
            else:
                return Response(status=404)
        elif meal_plan_id and not snack_id:
            extended_meal_plan_snacks: Optional[
                list[Extended_Meal_Plan_Snack_Domain]
            ] = Extended_Meal_Plan_Snack_Service(
                meal_plan_snack_repository=Meal_Plan_Snack_Repository(db=db)
            ).get_specific_extended_meal_plan_snacks(
                meal_plan_id=meal_plan_id
            )
            if extended_meal_plan_snacks:
                meal_plan_snack_DTOs = [
                    Extended_Meal_Plan_Snack_DTO(extended_meal_plan_snack_domain=x)
                    for x in extended_meal_plan_snacks
                ]
                serialized_meal_plan_snack_DTOs = [
                    x.serialize() for x in meal_plan_snack_DTOs
                ]
                return jsonify(serialized_meal_plan_snack_DTOs), 200
            else:
                return jsonify([]), 200
        else:
            extended_meal_plan_snack = Extended_Meal_Plan_Snack_Service(
                meal_plan_snack_repository=Meal_Plan_Snack_Repository(db=db)
            ).get_extended_meal_plan_snack(
                meal_plan_snack_id=None, meal_plan_id=meal_plan_id, snack_id=snack_id
            )
            if extended_meal_plan_snack:
                meal_plan_snack_DTO = Extended_Meal_Plan_Snack_DTO(
                    extended_meal_plan_snack_domain=extended_meal_plan_snack
                )
                serialized_meal_plan_snack_DTO = meal_plan_snack_DTO.serialize()
                return jsonify(serialized_meal_plan_snack_DTO), 200
            else:
                return Response(status=404)
    elif request.method == "PUT":
        ephemeral_meal_plan_snack = json.loads(request.data)

        # Get new quantity values for recipe ingredients to compute changes to nutrient amounts
        updated_recipe = ephemeral_meal_plan_snack["recipe"]
        updated_recipe_dtos = [
            Recipe_Ingredient_DTO(recipe_ingredient_json=x) for x in updated_recipe
        ]
        updated_meal_plan_snack = Extended_Meal_Plan_Snack_Service(
            meal_plan_snack_repository=Meal_Plan_Snack_Repository(db=db)
        ).compute_new_meal_plan_snack(
            meal_plan_snack_id=ephemeral_meal_plan_snack["id"],
            updated_recipe=updated_recipe_dtos,
        )

        updated_meal_plan_snack_dto = Extended_Meal_Plan_Snack_DTO(
            extended_meal_plan_snack_domain=updated_meal_plan_snack
        )
        return jsonify(updated_meal_plan_snack_dto.serialize()), 200
    else:
        return Response(status=405)


@app.route("/api/staged_schedule_snack", methods=["POST", "GET"])
def staged_schedule_snack() -> Response:
    from repository.Staged_Schedule_Snack_Repository import (
        Staged_Schedule_Snack_Repository,
    )
    from service.Staged_Schedule_Snack_Service import Staged_Schedule_Snack_Service
    from dto.Staged_Schedule_Snack_DTO import Staged_Schedule_Snack_DTO

    if request.method == "POST":
        staged_schedule_snacks_JSON = json.loads(request.data)
        staged_schedule_snack_DTOs = [
            Staged_Schedule_Snack_DTO(staged_schedule_snack_json=x)
            for x in staged_schedule_snacks_JSON
        ]
        Staged_Schedule_Snack_Service(
            staged_schedule_snack_repository=Staged_Schedule_Snack_Repository(db=db)
        ).create_staged_schedule_snacks(
            staged_schedule_snack_dtos=staged_schedule_snack_DTOs
        )
        return Response(status=201)

    elif request.method == "GET":
        staged_client_id = request.args.get("staged_client_id")
        staged_schedule_snack_domains = Staged_Schedule_Snack_Service(
            staged_schedule_snack_repository=Staged_Schedule_Snack_Repository(db=db)
        ).get_staged_schedule_snacks(staged_client_id=staged_client_id)
        staged_schedule_snack_DTOs = [
            Staged_Schedule_Snack_DTO(staged_schedule_snack_domain=x)
            for x in staged_schedule_snack_domains
        ]
        return jsonify([x.serialize() for x in staged_schedule_snack_DTOs]), 200
    else:
        return Response(status=405)


@app.route("/api/extended_staged_schedule_snack", methods=["GET"])
def extended_staged_schedule_snack() -> Response:
    from repository.Staged_Schedule_Snack_Repository import (
        Staged_Schedule_Snack_Repository,
    )
    from service.Extended_Staged_Schedule_Snack_Service import (
        Extended_Staged_Schedule_Snack_Service,
    )
    from domain.Extended_Staged_Schedule_Snack_Domain import (
        Extended_Staged_Schedule_Snack_Domain,
    )
    from dto.Extended_Staged_Schedule_Snack_DTO import (
        Extended_Staged_Schedule_Snack_DTO,
    )

    if request.method == "GET":
        staged_client_id = request.args.get("staged_client_id")
        extended_staged_schedule_snack_domains: Optional[
            list[Extended_Staged_Schedule_Snack_Domain]
        ] = Extended_Staged_Schedule_Snack_Service(
            staged_schedule_snack_repository=Staged_Schedule_Snack_Repository(db=db)
        ).get_staged_schedule_snacks(
            staged_client_id=staged_client_id
        )
        if extended_staged_schedule_snack_domains:
            staged_schedule_snack_dtos = [
                Extended_Staged_Schedule_Snack_DTO(
                    extended_staged_schedule_snack_domain=x
                )
                for x in extended_staged_schedule_snack_domains
            ]
            serialized_staged_schedule_snack_DTOs = [
                x.serialize() for x in staged_schedule_snack_dtos
            ]
        return jsonify(serialized_staged_schedule_snack_DTOs), 200
    else:
        return Response(status=405)


@app.route("/api/dietitian_prepayment", methods=["POST"])
def dietitian_prepayment() -> Response:
    from repository.Dietitian_Prepayment_Repository import (
        Dietitian_Prepayment_Repository,
    )
    from repository.Discount_Repository import Discount_Repository
    from repository.Prepaid_Order_Discount_Repository import (
        Prepaid_Order_Discount_Repository,
    )
    from repository.COGS_Repository import COGS_Repository

    from service.Dietitian_Prepayment_Service import Dietitian_Prepayment_Service
    from service.Discount_Service import Discount_Service
    from service.Prepaid_Order_Discount_Service import Prepaid_Order_Discount_Service
    from service.COGS_Service import COGS_Service
    from service.Shippo_Service import Shippo_Service

    if request.method == "POST":
        prepayment_data = json.loads(request.data)

        prepaid_order_discount_code = prepayment_data["discount_code"]
        num_meals = prepayment_data["num_meals"]
        num_snacks = prepayment_data["num_snacks"]
        staged_client_id = prepayment_data["staged_client_id"]
        dietitian_id = prepayment_data["dietitian_id"]
        stripe_payment_intent_id = prepayment_data["stripe_payment_intent_id"]
        zipcode = prepayment_data["zipcode"]

        shipping_rate = Shippo_Service().get_shipping_rate(zipcode=zipcode)
        cost_per_meal = COGS_Service(
            cogs_repository=COGS_Repository(db=db)
        ).get_meal_cost(
            num_meals=num_meals,
            num_snacks=num_snacks,
            shipping_rate=shipping_rate,
        )
        meal_price = COGS_Service(
            cogs_repository=COGS_Repository(db=db)
        ).get_meal_price(meal_cost=cost_per_meal)
        snack_price = COGS_Service(
            cogs_repository=COGS_Repository(db=db)
        ).get_snack_price(meal_price=meal_price)
        shipping_cost = COGS_Service(
            cogs_repository=COGS_Repository(db=db)
        ).get_shipping_cost(
            num_meals=num_meals,
            num_snacks=num_snacks,
            shipping_rate=shipping_rate,
        )

        Dietitian_Prepayment_Service(
            dietitian_prepayment_repository=Dietitian_Prepayment_Repository(db=db)
        ).create_dietitian_prepayment(
            num_meals=num_meals,
            num_snacks=num_snacks,
            discount_code=prepaid_order_discount_code,
            staged_client_id=staged_client_id,
            dietitian_id=dietitian_id,
            stripe_payment_intent_id=stripe_payment_intent_id,
            meal_price=meal_price,
            snack_price=snack_price,
            shipping_cost=shipping_cost,
            discount_service=Discount_Service(
                discount_repository=Discount_Repository(db=db)
            ),
            prepaid_order_discount_service=Prepaid_Order_Discount_Service(
                prepaid_order_discount_repository=Prepaid_Order_Discount_Repository(
                    db=db
                )
            ),
        )
        return Response(status=201)
    else:
        return Response(status=405)


@app.route(
    "/api/meal_subscription/<string:meal_subscription_id>", methods=["GET", "PUT"]
)
def specific_meal_subscription(meal_subscription_id: str) -> Response:
    from repository.Meal_Subscription_Repository import Meal_Subscription_Repository
    from service.Meal_Subscription_Service import Meal_Subscription_Service
    from service.Stripe_Service import Stripe_Service
    from dto.Meal_Subscription_DTO import Meal_Subscription_DTO

    if request.method == "GET":
        meal_subscription_domain = Meal_Subscription_Service(
            meal_subscription_repository=Meal_Subscription_Repository(db=db)
        ).get_meal_subscription(meal_subscription_id=meal_subscription_id)
        meal_subscription_dto = Meal_Subscription_DTO(
            meal_subscription_domain=meal_subscription_domain
        )
        return jsonify(meal_subscription_dto.serialize()), 200
    if request.method == "PUT":
        if request.headers.get("update") == "deactivate":
            Meal_Subscription_Service(
                meal_subscription_repository=Meal_Subscription_Repository(db=db)
            ).deactivate_meal_subscription(meal_subscription_id=meal_subscription_id)

        elif request.headers.get("update") == "pause":
            Meal_Subscription_Service(
                meal_subscription_repository=Meal_Subscription_Repository(db=db)
            ).pause_meal_subscription(
                meal_subscription_id=meal_subscription_id,
                stripe_service=Stripe_Service(),
            )

        elif request.headers.get("update") == "unpause":
            Meal_Subscription_Service(
                meal_subscription_repository=Meal_Subscription_Repository(db=db)
            ).unpause_meal_subscription(
                meal_subscription_id=meal_subscription_id,
                stripe_service=Stripe_Service(),
            )

        return Response(status=204)

    else:
        return Response(status=405)


@app.route("/api/meal_subscription", methods=["POST", "GET"])
# @requires_auth
def meal_subscription() -> Response:
    from repository.Meal_Subscription_Repository import Meal_Subscription_Repository
    from service.Meal_Subscription_Service import Meal_Subscription_Service
    from domain.Meal_Subscription_Domain import Meal_Subscription_Domain
    from dto.Meal_Subscription_DTO import Meal_Subscription_DTO

    if request.method == "POST":
        meal_subscription_data = json.loads(request.data)
        meal_subscription_DTO = Meal_Subscription_DTO(
            meal_subscription_json=meal_subscription_data
        )
        prev_meal_subscription_domain = Meal_Subscription_Service(
            meal_subscription_repository=Meal_Subscription_Repository(db=db)
        ).get_client_meal_subscription(client_id=meal_subscription_DTO.client_id)
        if (
            prev_meal_subscription_domain
            and prev_meal_subscription_domain.active == False
        ):
            created_meal_subscription_domain = Meal_Subscription_Service(
                meal_subscription_repository=Meal_Subscription_Repository(db=db)
            ).update_meal_subscription(meal_subscription_dto=meal_subscription_DTO)
        else:
            created_meal_subscription_domain = Meal_Subscription_Service(
                meal_subscription_repository=Meal_Subscription_Repository(db=db)
            ).create_meal_subscription(meal_subscription_dto=meal_subscription_DTO)
        created_meal_subscription_dto = Meal_Subscription_DTO(
            meal_subscription_domain=created_meal_subscription_domain
        )
        return jsonify(created_meal_subscription_dto.serialize()), 201

    elif request.method == "GET":
        client_id: str | None = request.args.get("client_id")
        if client_id:
            meal_subscription_domain: Optional[
                Meal_Subscription_Domain
            ] = Meal_Subscription_Service(
                meal_subscription_repository=Meal_Subscription_Repository(db=db)
            ).get_client_meal_subscription(
                client_id=client_id
            )

            # Client will always have 1 and only 1 active meal subscription
            if meal_subscription_domain:
                meal_subscription_DTO = Meal_Subscription_DTO(
                    meal_subscription_domain=meal_subscription_domain
                )
                return jsonify(meal_subscription_DTO.serialize()), 200
            # Otherwise client_id is invalid and return 404
            else:
                return Response(status=404)
        else:
            dietitian_id = request.args.get("dietitian_id")
            meal_subscription_domains: Optional[
                list[Meal_Subscription_Domain]
            ] = Meal_Subscription_Service(
                meal_subscription_repository=Meal_Subscription_Repository(db=db)
            ).get_dietitian_meal_subscriptions(
                dietitian_id=dietitian_id
            )
            if meal_subscription_domains:
                meal_subscription_DTOs = [
                    Meal_Subscription_DTO(meal_subscription_domain=x)
                    for x in meal_subscription_domains
                ]
                serialized_meal_subscription_DTOs = [
                    x.serialize() for x in meal_subscription_DTOs
                ]
                return jsonify(serialized_meal_subscription_DTOs), 200

            # New dietitian will not have any client meal subscriptions
            # 204 code is used to indicate that the request has succeeded but that there is no content to send in the response
            else:
                return Response(status=204)
    else:
        return Response(status=405)


@app.route("/api/meal_plan", methods=["GET"])
# @requires_auth
def meal_plan() -> Response:
    from service.Meal_Plan_Service import Meal_Plan_Service
    from repository.Meal_Plan_Repository import Meal_Plan_Repository
    from domain.Meal_Plan_Domain import Meal_Plan_Domain
    from dto.Meal_Plan_DTO import Meal_Plan_DTO

    if request.method == "GET":
        meal_plan_number = request.args.get("meal_plan_number")
        if not meal_plan_number:
            meal_plan_domains = Meal_Plan_Service(
                Meal_Plan_Repository(db=db)
            ).get_meal_plans()
            meal_plan_DTOs = [
                Meal_Plan_DTO(meal_plan_domain=x) for x in meal_plan_domains
            ]
            serialized_meal_plan_DTOs = [x.serialize() for x in meal_plan_DTOs]
            return jsonify(serialized_meal_plan_DTOs), 200
        else:
            meal_plan_domain = Meal_Plan_Service(
                Meal_Plan_Repository(db=db)
            ).get_meal_plan(meal_plan_number=meal_plan_number)
            meal_plan_DTO = Meal_Plan_DTO(meal_plan_domain=meal_plan_domain)
            return jsonify(meal_plan_DTO.serialize()), 200

    else:
        return Response(status=405)


@app.route("/api/extended_order_meal", methods=["GET"])
def extended_order_meal() -> Response:
    from repository.Order_Meal_Repository import Order_Meal_Repository
    from service.Extended_Order_Meal_Service import Extended_Order_Meal_Service
    from domain.Extended_Order_Meal_Domain import Extended_Order_Meal_Domain
    from dto.Extended_Order_Meal_DTO import Extended_Order_Meal_DTO

    if request.method == "GET":
        meal_subscription_id = request.args.get("meal_subscription_id")
        extended_order_meals: Optional[
            list[Extended_Order_Meal_Domain]
        ] = Extended_Order_Meal_Service(
            order_meal_repository=Order_Meal_Repository(db=db)
        ).get_extended_order_meals(
            meal_subscription_id=meal_subscription_id
        )
        if extended_order_meals:
            extended_order_meal_DTOs = [
                Extended_Order_Meal_DTO(extended_order_meal_domain=x)
                for x in extended_order_meals
            ]
            serialized_order_meal_DTOs = [
                x.serialize() for x in extended_order_meal_DTOs
            ]
            return jsonify(serialized_order_meal_DTOs), 200
        # Client will always have at least 6 order meals
        else:
            return Response(status=404)
    else:
        return Response(status=405)


@app.route("/api/order_meal", methods=["POST", "GET"])
def order_meal() -> Response:
    from service.Order_Meal_Service import Order_Meal_Service
    from repository.Order_Meal_Repository import Order_Meal_Repository
    from domain.Order_Meal_Domain import Order_Meal_Domain
    from dto.Order_Meal_DTO import Order_Meal_DTO

    if request.method == "POST":
        order_meals_json = json.loads(request.data)
        order_meal_DTOs = [Order_Meal_DTO(order_meal_json=x) for x in order_meals_json]
        Order_Meal_Service(
            order_meal_repository=Order_Meal_Repository(db=db)
        ).create_order_meals(order_meal_dtos=order_meal_DTOs)
        return Response(status=201)
    elif request.method == "GET":
        meal_subscription_id: str = request.args.get("meal_subscription_id")
        order_meal_domains: Optional[list[Order_Meal_Domain]] = Order_Meal_Service(
            order_meal_repository=Order_Meal_Repository(db=db)
        ).get_order_meals(meal_subscription_id=meal_subscription_id)
        if order_meal_domains:
            order_meal_DTOs = [
                Order_Meal_DTO(order_meal_domain=x) for x in order_meal_domains
            ]
            serialized_order_meal_DTOs = [x.serialize() for x in order_meal_DTOs]

            return jsonify(serialized_order_meal_DTOs), 200
        else:
            return Response(status=204)
    else:
        return Response(status=405)


@app.route("/api/cogs", methods=["GET", "PUT"])
def cogs() -> Response:
    from repository.COGS_Repository import COGS_Repository
    from service.COGS_Service import COGS_Service
    from dto.COGS_DTO import COGS_DTO
    from helpers.db.create_cogs import create_cogs

    if request.method == "GET":
        cogs_list = COGS_Service(cogs_repository=COGS_Repository(db=db)).get_cogs()
        cogs_dtos = [COGS_DTO(cogs_domain=x) for x in cogs_list]
        serialized_cogs = [x.serialize() for x in cogs_dtos]
        return jsonify(serialized_cogs), 200
    elif request.method == "PUT":
        COGS_Service(cogs_repository=COGS_Repository(db=db)).delete_all_cogs()
        create_cogs(db=db)
        return Response(status=204)
    else:
        return Response(status=405)


@app.route("/api/eating_disorder", methods=["GET"])
def eating_disorder() -> Response:
    from repository.Eating_Disorder_Repository import Eating_Disorder_Repository
    from service.Eating_Disorder_Service import Eating_Disorder_Service
    from dto.Eating_Disorder_DTO import Eating_Disorder_DTO

    if request.method == "GET":
        eating_disorder_list = Eating_Disorder_Service(
            eating_disorder_repository=Eating_Disorder_Repository(db=db)
        ).get_eating_disorders()
        eating_disorder_dtos = [
            Eating_Disorder_DTO(eating_disorder_domain=x) for x in eating_disorder_list
        ]
        serialized_eating_disorder = [x.serialize() for x in eating_disorder_dtos]
        return jsonify(serialized_eating_disorder), 200
    else:
        return Response(status=405)


@app.route("/api/shippo/shipping_rate", methods=["GET"])
def shipping_cost() -> Response:
    from service.Shippo_Service import Shippo_Service

    zipcode = request.args.get("zipcode")
    shipping_rate = Shippo_Service().get_shipping_rate(zipcode=zipcode)
    if request.method == "GET":
        return jsonify(shipping_rate), 200
    else:
        return Response(status=405)


@app.route(
    "/api/meal_subscription/<string:meal_subscription_id>/first_week", methods=["GET"]
)
def is_first_week(meal_subscription_id: UUID) -> Response:
    from service.Scheduled_Order_Meal_Service import Scheduled_Order_Meal_Service
    from repository.Scheduled_Order_Meal_Repository import (
        Scheduled_Order_Meal_Repository,
    )

    if request.method == "GET":
        is_first_week = Scheduled_Order_Meal_Service(
            scheduled_order_meal_repository=Scheduled_Order_Meal_Repository(db=db)
        ).check_if_first_week_of_meals(meal_subscription_id=meal_subscription_id)
        return jsonify(is_first_week), 200
    else:
        return Response(status=405)


@app.route("/api/meal_subscription/skip_week", methods=["PUT"])
def skip_week() -> Response:
    from service.Date_Service import Date_Service
    from service.Scheduled_Order_Meal_Service import Scheduled_Order_Meal_Service
    from service.Stripe_Service import Stripe_Service
    from repository.Scheduled_Order_Meal_Repository import (
        Scheduled_Order_Meal_Repository,
    )

    if request.method == "PUT":
        # This indicates that the user is unskipping a week, rather than skipping a week
        skipping_data = json.loads(request.data)
        unskipping: bool = skipping_data["unskipping"]
        meal_subscription_id: UUID = skipping_data["meal_subscription_id"]
        stripe_subscription_id: str = skipping_data["stripe_subscription_id"]
        delivery_date_timestamp: float = skipping_data["delivery_date"]

        # If skipping, skip the week in stripe + database, and vice-versa
        if not unskipping:
            Scheduled_Order_Meal_Service(
                scheduled_order_meal_repository=Scheduled_Order_Meal_Repository(db=db)
            ).skip_weekly_scheduled_order_meals(
                meal_subscription_id=meal_subscription_id,
                delivery_date=delivery_date_timestamp,
            )
            Stripe_Service().skip_week(
                stripe_subscription_id=stripe_subscription_id,
                delivery_date=delivery_date_timestamp,
                date_service=Date_Service(),
            )
        else:
            Scheduled_Order_Meal_Service(
                scheduled_order_meal_repository=Scheduled_Order_Meal_Repository(db=db)
            ).unskip_weekly_scheduled_order_meals(
                meal_subscription_id=meal_subscription_id,
                delivery_date=delivery_date_timestamp,
            )
            Stripe_Service().unskip_week(stripe_subscription_id=stripe_subscription_id)
        return Response(status=204)

    else:
        return Response(status=405)


@app.route("/api/meal_subscription_invoice", methods=["GET", "POST"])
def meal_subscription_invoice() -> Response:
    from repository.Client_Repository import Client_Repository
    from repository.Meal_Subscription_Invoice_Repository import (
        Meal_Subscription_Invoice_Repository,
    )
    from repository.Meal_Subscription_Repository import Meal_Subscription_Repository
    from repository.Schedule_Meal_Repository import (
        Schedule_Meal_Repository,
    )
    from repository.Schedule_Snack_Repository import Schedule_Snack_Repository
    from repository.Meal_Shipment_Repository import Meal_Shipment_Repository
    from repository.Discount_Repository import Discount_Repository

    from service.Client_Service import Client_Service
    from service.Schedule_Meal_Service import Schedule_Meal_Service
    from service.Schedule_Snack_Service import Schedule_Snack_Service
    from service.Meal_Subscription_Invoice_Service import (
        Meal_Subscription_Invoice_Service,
    )
    from service.Meal_Subscription_Service import Meal_Subscription_Service
    from service.Shippo_Service import Shippo_Service
    from service.Date_Service import Date_Service
    from service.Discount_Service import Discount_Service
    from service.Order_Calc_Service import Order_Calc_Service
    from service.Email_Service import Email_Service
    from service.GCP_Secret_Manager_Service import GCP_Secret_Manager_Service

    from dto.Meal_Subscription_Invoice_DTO import Meal_Subscription_Invoice_DTO

    if request.method == "GET":
        meal_subscription_id = request.args.get("meal_subscription_id")
        requested_meal_subscription_invoice_domains = Meal_Subscription_Invoice_Service(
            meal_subscription_invoice_repository=Meal_Subscription_Invoice_Repository(
                db=db
            )
        ).get_meal_subscription_invoices(meal_subscription_id=meal_subscription_id)
        if requested_meal_subscription_invoice_domains:
            requested_meal_subscription_invoice_DTOs = [
                Meal_Subscription_Invoice_DTO(meal_subscription_invoice_domain=x)
                for x in requested_meal_subscription_invoice_domains
            ]
            return (
                jsonify(
                    [x.serialize() for x in requested_meal_subscription_invoice_DTOs]
                ),
                200,
            )
        else:
            return Response(status=404)

    elif request.method == "POST":
        from repository.COGS_Repository import COGS_Repository
        from service.COGS_Service import COGS_Service

        meal_subscription_invoice_data = json.loads(request.data)
        discount_code: Optional[str] = request.headers.get("discount_code")
        discount_percentage = False
        if discount_code:
            discount_percentage = (
                Discount_Service(discount_repository=Discount_Repository(db=db))
                .get_discount(discount_code=discount_code)
                .discount_percentage
            )

        meal_subscription_invoice_dto = Meal_Subscription_Invoice_DTO(
            meal_subscription_invoice_json=meal_subscription_invoice_data
        )
        associated_meal_subscription = Meal_Subscription_Service(
            meal_subscription_repository=Meal_Subscription_Repository(db=db)
        ).get_meal_subscription(
            meal_subscription_id=meal_subscription_invoice_dto.meal_subscription_id
        )

        associated_schedule_meals = Schedule_Meal_Service(
            schedule_meal_repository=Schedule_Meal_Repository(db=db)
        ).get_schedule_meals(meal_subscription_id=associated_meal_subscription.id)
        associated_schedule_snacks = Schedule_Snack_Service(
            schedule_snack_repository=Schedule_Snack_Repository(db=db)
        ).get_schedule_snacks(
            meal_subscription_id=associated_meal_subscription.id,
        )

        if associated_schedule_snacks:
            num_snacks = len(associated_schedule_snacks)
        else:
            num_snacks = 0

        cost_per_meal = COGS_Service(
            cogs_repository=COGS_Repository(db=db)
        ).get_meal_cost(
            num_meals=len(associated_schedule_meals),
            num_snacks=num_snacks,
            shipping_rate=associated_meal_subscription.shipping_rate,
        )
        meal_price = COGS_Service(
            cogs_repository=COGS_Repository(db=db)
        ).get_meal_price(meal_cost=cost_per_meal)
        num_items = COGS_Service(cogs_repository=COGS_Repository(db=db)).get_num_items(
            num_meals=len(associated_schedule_meals),
            num_snacks=num_snacks,
        )
        shipping_cost = COGS_Service(
            cogs_repository=COGS_Repository(db=db)
        ).get_shipping_cost(
            num_meals=len(associated_schedule_meals),
            num_snacks=num_snacks,
            shipping_rate=associated_meal_subscription.shipping_rate,
        )
        new_meal_subscription_invoice = Meal_Subscription_Invoice_Service(
            meal_subscription_invoice_repository=Meal_Subscription_Invoice_Repository(
                db=db
            )
        ).create_meal_subscription_invoice(
            meal_subscription_invoice_dto=meal_subscription_invoice_dto,
            meal_price=meal_price,
            shipping_cost=shipping_cost,
            num_items=num_items,
            order_calc_service=Order_Calc_Service(),
            discount_percentage=discount_percentage,
        )

        # Create meal_shipment, using Shippo service because our meal_shipment is dependent on values generated during Shippo shipment creation
        associated_client = Client_Service(
            client_repository=Client_Repository(db=db)
        ).get_client(client_id=associated_meal_subscription.client_id)
        meal_shipment = Shippo_Service().create_shipment(
            meal_subscription_invoice_id=new_meal_subscription_invoice.id,
            client=associated_client,
            meal_shipment_repository=Meal_Shipment_Repository(db=db),
        )

        # Get values needed to send client confirmation email
        upcoming_delivery_date = Date_Service().get_current_week_delivery_date()

        cutoff_date = datetime.fromtimestamp(
            Date_Service().get_current_week_cutoff(
                current_delivery_date=upcoming_delivery_date
            ),
            tz=timezone.utc,
        )
        # Send client confirmation email after creating shipment so as to include the tracking number
        Email_Service(
            gcp_secret_manager_service=GCP_Secret_Manager_Service(),
        ).send_confirmation_email(
            user_type="Client",
            user=associated_client,
            delivery_date=datetime.fromtimestamp(
                upcoming_delivery_date, tz=timezone.utc
            ),
            cutoff_date=cutoff_date,
            tracking_url=meal_shipment.tracking_url,
        )

        new_meal_subscription_invoice_dto = Meal_Subscription_Invoice_DTO(
            meal_subscription_invoice_domain=new_meal_subscription_invoice
        )

        serialized_new_meal_subscription_invoice_dto = (
            new_meal_subscription_invoice_dto.serialize()
        )
        return jsonify(serialized_new_meal_subscription_invoice_dto), 201
    else:
        return Response(status=405)


@app.route("/api/sales_tax", methods=["GET"])
def sales_tax() -> Response:
    from service.State_Sales_Tax_Service import State_Sales_Tax_Service
    from repository.State_Sales_Tax_Repository import State_Sales_Tax_Repository
    from domain.State_Sales_Tax_Domain import State_Sales_Tax_Domain

    if request.method == "GET":
        state: str | None = request.headers.get("state")
        sales_tax: State_Sales_Tax_Domain = State_Sales_Tax_Service(
            state_sales_tax_repository=State_Sales_Tax_Repository(db=db)
        ).get_sales_tax(state)
        sales_tax_rate = sales_tax.sales_tax_percentage
        return jsonify(sales_tax_rate), 200
    else:
        return Response(status=405)


@app.route("/api/order_discount", methods=["POST"])
def order_discount() -> Response:
    from service.Order_Discount_Service import Order_Discount_Service
    from repository.Order_Discount_Repository import Order_Discount_Repository
    from dto.Order_Discount_DTO import Order_Discount_DTO

    if request.method == "POST":
        order_discount_json = json.loads(request.data)
        order_discount_dto = Order_Discount_DTO(order_discount_json=order_discount_json)
        Order_Discount_Service(
            order_discount_repository=Order_Discount_Repository(db=db)
        ).create_order_discount(order_discount_dto=order_discount_dto)
        return Response(status=201)


@app.route("/api/discount", methods=["GET"])
def verify_discount() -> Response:
    from service.Discount_Service import Discount_Service
    from repository.Discount_Repository import Discount_Repository
    from domain.Discount_Domain import Discount_Domain
    from dto.Discount_DTO import Discount_DTO

    if request.method == "GET":
        discount_code = request.headers.get("discount")
        discount: Optional[Discount_Domain] = Discount_Service(
            discount_repository=Discount_Repository(db=db)
        ).verify_discount_code(discount_code=discount_code)
        if discount:
            discount_dto = Discount_DTO(discount_domain=discount)
            return jsonify(discount_dto.serialize()), 200
        else:
            return Response(status=404)
    else:
        return Response(status=405)


@app.route("/api/stripe/payment_method", methods=["GET", "PUT"])
def stripe_payment_methods() -> Response:
    from service.Stripe_Service import Stripe_Service

    stripe_customer_id = request.args.get("stripe_customer_id")
    if request.method == "GET":
        payment_methods = Stripe_Service().get_payment_methods(
            stripe_customer_id=stripe_customer_id
        )
        response = {
            "last4": payment_methods.data[0].card.last4,
            "exp_month": payment_methods.data[0].card.exp_month,
            "exp_year": payment_methods.data[0].card.exp_year,
        }
        return jsonify(response), 200
    elif request.method == "PUT":
        stripe_payment_method_id = request.headers.get("stripe-payment-method-id")
        stripe_subscription_id = request.headers.get("stripe-subscription-id")
        payment_method_update = Stripe_Service().update_payment_method(
            stripe_customer_id=stripe_customer_id,
            stripe_payment_method_id=stripe_payment_method_id,
            stripe_subscription_id=stripe_subscription_id,
        )
        if payment_method_update:
            return Response(status=204)
        else:
            return Response(status=400)


@app.route(
    "/api/stripe/get_subscription_details/<string:subscription_id>/", methods=["GET"]
)
def get_subscription_details(subscription_id: str):
    try:
        subscription = stripe.Subscription.retrieve(subscription_id)
        return jsonify(subscription), 200
    except stripe.error.StripeError as e:
        error_message = e.user_message or str(e)
        return False, error_message


@app.route("/api/stripe/get_customer_details/<string:customer_id>/", methods=["GET"])
def get_customer_details(customer_id):
    try:
        customer = stripe.Customer.retrieve(customer_id)
        return jsonify(customer), 200
    except stripe.error.StripeError as e:
        error_message = e.user_message or str(e)
        return False, error_message


@app.route("/api/stripe/check_last_payment/<string:customer_id>/", methods=["GET"])
def check_last_payment(customer_id):
    try:
        invoices = stripe.Invoice.list(customer=customer_id)
        last_invoice = invoices.data[0]
        last_invoice_status = last_invoice.status

        if last_invoice_status == "failed":
            response = {
                "status": "failed",
                "message": "The last payment for this customer has failed.",
            }
        else:
            response = {
                "status": "success",
                "message": "The last payment for this customer was successful.",
            }

        return jsonify(response), 200

    except stripe.error.StripeError as e:
        # Handle any Stripe API errors
        error_message = str(e)
        response = {
            "status": "error",
            "message": "An error occurred while checking the payment status.",
            "error": error_message,
        }
        return jsonify(response), 500


@app.route(
    "/api/stripe/get_client_payment_invoices/<string:customer_id>/", methods=["GET"]
)
def get_client_payment_invoices(customer_id):
    try:
        invoices = stripe.Invoice.list(customer=customer_id, limit=10)
        invoice_details = []

        for invoice in invoices.data:
            invoice_url = invoice.hosted_invoice_url
            invoice_price = invoice.amount_due
            invoice_created = datetime.fromtimestamp(invoice.created).strftime(
                "%Y-%m-%d"
            )
            invoice_number = invoice.number
            last_invoice_status = invoice.status
            if last_invoice_status == "failed":
                invoice_status = "failed"
            else:
                invoice_status = "success"

            invoice_details.append(
                {
                    "invoice_url": invoice_url,
                    "invoice_price": invoice_price,
                    "invoice_created": invoice_created,
                    "invoice_number": invoice_number,
                    "invoice_status": invoice_status,
                }
            )

        response = {
            "status": "success",
            "message": "Invoice details retrieved successfully.",
            "invoices": invoice_details,
        }

        return jsonify(response), 200

    except stripe.error.StripeError as e:
        # Handle any Stripe API errors
        error_message = str(e)
        response = {
            "status": "error",
            "message": "An error occurred while retrieving the invoice details.",
            "error": error_message,
        }
        return jsonify(response), 500


@app.route("/api/stripe/payment_intent", methods=["POST"])
def create_stripe_payment_intent() -> Response:
    from repository.Discount_Repository import Discount_Repository
    from repository.COGS_Repository import COGS_Repository

    from service.Discount_Service import Discount_Service
    from service.COGS_Service import COGS_Service
    from service.Stripe_Service import Stripe_Service
    from service.Order_Calc_Service import Order_Calc_Service
    from service.Shippo_Service import Shippo_Service

    if request.method == "POST":
        number_of_meals = request.headers.get("number_of_meals")
        number_of_snacks = request.headers.get("number_of_snacks")
        discount_code = request.headers.get("discount_code")
        zipcode = request.headers.get("zipcode")
        # If no discount code is provided, set to False so that it is not passed to Stripe_Service
        if discount_code == "":
            discount_percentage = False
        else:
            discount_percentage = (
                Discount_Service(discount_repository=Discount_Repository(db=db))
                .get_discount(discount_code=discount_code)
                .discount_percentage
            )
        shipping_rate = Shippo_Service().get_shipping_rate(zipcode=zipcode)
        meal_cost = COGS_Service(cogs_repository=COGS_Repository(db=db)).get_meal_cost(
            num_meals=number_of_meals,
            num_snacks=number_of_snacks,
            shipping_rate=shipping_rate,
        )
        meal_price = COGS_Service(
            cogs_repository=COGS_Repository(db=db)
        ).get_meal_price(meal_cost=meal_cost)
        snack_price = COGS_Service(
            cogs_repository=COGS_Repository(db=db)
        ).get_snack_price(meal_price=meal_price)

        shipping_rate = Shippo_Service().get_shipping_rate(zipcode=zipcode)
        shipping_cost = COGS_Service(
            cogs_repository=COGS_Repository(db=db)
        ).get_shipping_cost(
            num_meals=number_of_meals,
            num_snacks=number_of_snacks,
            shipping_rate=shipping_rate,
        )
        stripe_secret = Stripe_Service().create_payment_intent(
            number_of_meals=number_of_meals,
            number_of_snacks=number_of_snacks,
            meal_price=meal_price,
            snack_price=snack_price,
            shipping_cost=shipping_cost,
            order_calc_service=Order_Calc_Service(),
            discount_percentage=discount_percentage,
        )

        return jsonify(stripe_secret), 200
    else:
        return Response(status=405)


@app.route("/api/client/address", methods=["PUT"])
def update_client_address() -> Response:
    from service.Client_Service import Client_Service
    from repository.Client_Repository import Client_Repository
    from dto.Client_DTO import Client_DTO

    client_dto = Client_DTO(client_json=json.loads(request.data))
    if request.method == "PUT":
        Client_Service(client_repository=Client_Repository(db=db)).update_address(
            client_dto=client_dto
        )
        return Response(status=201)

    else:
        return Response(status=405)


@app.route("/api/dietitian/sample_trial_period", methods=["GET"])
def sample_trial_period() -> Response:
    if request.method == "GET":
        return jsonify(False), 200
    else:
        return Response(status=405)


@app.route("/api/meal_nutrient_stats", methods=["GET"])
def extended_meal_plan_meal_v2() -> Response:
    from repository.Meal_Plan_Meal_Repository import Meal_Plan_Meal_Repository
    from repository.Meal_Plan_Repository import Meal_Plan_Repository
    from service.Extended_Meal_Plan_Meal_Service import Extended_Meal_Plan_Meal_Service
    from service.Meal_Plan_Service import Meal_Plan_Service
    from service.Food_Nutrient_Stats_Service import Food_Nutrient_Stats_Service
    from domain.Extended_Meal_Plan_Meal_Domain import Extended_Meal_Plan_Meal_Domain
    from dto.Extended_Meal_Plan_Meal_DTO import Extended_Meal_Plan_Meal_DTO
    from dto.Food_Nutrient_Stats_DTO import Food_Nutrient_Stats_DTO

    if request.method == "GET":
        meal_plan_id = request.args.get("meal_plan_id")
        meal_id = request.args.get("meal_id")
        meal_plan_number = request.args.get("meal_plan_number")
        if not meal_id:
            if meal_plan_number:
                associated_meal_plan = Meal_Plan_Service(
                    meal_plan_repository=Meal_Plan_Repository(db=db)
                ).get_meal_plan(meal_plan_number=meal_plan_number)
                extended_meal_plan_meals = Extended_Meal_Plan_Meal_Service(
                    meal_plan_meal_repository=Meal_Plan_Meal_Repository(db=db)
                ).get_specific_extended_meal_plan_meals(
                    meal_plan_id=associated_meal_plan.id
                )
                if extended_meal_plan_meals:
                    meal_plan_meal_DTOs = [
                        Extended_Meal_Plan_Meal_DTO(extended_meal_plan_meal_domain=x)
                        for x in extended_meal_plan_meals
                    ]
                else:
                    return Response(status=404)
            elif not meal_plan_id and not meal_id:
                extended_meal_plan_meals: Optional[
                    list[Extended_Meal_Plan_Meal_Domain]
                ] = Extended_Meal_Plan_Meal_Service(
                    meal_plan_meal_repository=Meal_Plan_Meal_Repository(db=db)
                ).get_extended_meal_plan_meals()
                if extended_meal_plan_meals:
                    meal_plan_meal_DTOs = [
                        Extended_Meal_Plan_Meal_DTO(extended_meal_plan_meal_domain=x)
                        for x in extended_meal_plan_meals
                    ]

                else:
                    return Response(status=404)
            elif meal_plan_id and not meal_id:
                extended_meal_plan_meals = Extended_Meal_Plan_Meal_Service(
                    meal_plan_meal_repository=Meal_Plan_Meal_Repository(db=db)
                ).get_specific_extended_meal_plan_meals(meal_plan_id=meal_plan_id)
                if extended_meal_plan_meals:
                    meal_plan_meal_DTOs = [
                        Extended_Meal_Plan_Meal_DTO(extended_meal_plan_meal_domain=x)
                        for x in extended_meal_plan_meals
                    ]

                else:
                    return Response(status=404)
            # Return compressed meal plan meals
            food_nutrient_stats_dtos: list[Food_Nutrient_Stats_DTO] = []
            for meal_plan_meal_dto in meal_plan_meal_DTOs:
                food_nutrient_stats_dtos.append(
                    Food_Nutrient_Stats_Service().extract_nutrient_stats(
                        extended_meal_plan_food=meal_plan_meal_dto
                    )
                )
            serialized_food_nutrient_stats_dtos = [
                x.serialize() for x in food_nutrient_stats_dtos
            ]
            return jsonify(serialized_food_nutrient_stats_dtos), 200

        # Make sure this method doesn't need to be updated to compressed format
        else:
            # Only returning single meal plan meal
            extended_meal_plan_meal = Extended_Meal_Plan_Meal_Service(
                meal_plan_meal_repository=Meal_Plan_Meal_Repository(db=db)
            ).get_extended_meal_plan_meal(
                meal_plan_meal_id=None, meal_plan_id=meal_plan_id, meal_id=meal_id
            )
            if extended_meal_plan_meal:
                meal_plan_meal_DTO = Extended_Meal_Plan_Meal_DTO(
                    extended_meal_plan_meal_domain=extended_meal_plan_meal
                )

                serialized_meal_plan_meal_DTO = meal_plan_meal_DTO.serialize()
                return jsonify(serialized_meal_plan_meal_DTO), 200
            else:
                return jsonify([]), 200

    else:
        return Response(status=405)


@app.route("/api/snack_nutrient_stats", methods=["GET"])
def extended_meal_plan_snack_v2() -> Response:
    from repository.Meal_Plan_Snack_Repository import Meal_Plan_Snack_Repository
    from service.Extended_Meal_Plan_Snack_Service import (
        Extended_Meal_Plan_Snack_Service,
    )
    from service.Food_Nutrient_Stats_Service import Food_Nutrient_Stats_Service
    from dto.Extended_Meal_Plan_Snack_DTO import Extended_Meal_Plan_Snack_DTO
    from dto.Food_Nutrient_Stats_DTO import Food_Nutrient_Stats_DTO

    if request.method == "GET":
        snack_id = request.args.get("snack_id")
        if snack_id:
            extended_meal_plan_snack = Extended_Meal_Plan_Snack_Service(
                meal_plan_snack_repository=Meal_Plan_Snack_Repository(db=db)
            ).get_extended_meal_plan_snack(snack_id=snack_id)
            if extended_meal_plan_snack:
                meal_plan_snack_DTO = Extended_Meal_Plan_Snack_DTO(
                    extended_meal_plan_snack_domain=extended_meal_plan_snack
                )

                serialized_meal_plan_snack_DTO = meal_plan_snack_DTO.serialize()
                return jsonify(serialized_meal_plan_snack_DTO), 200
            else:
                return jsonify([]), 200
        else:
            extended_meal_plan_snacks = (
                extended_meal_plan_snack
            ) = Extended_Meal_Plan_Snack_Service(
                meal_plan_snack_repository=Meal_Plan_Snack_Repository(db=db)
            ).get_standard_extended_meal_plan_snacks()
            extended_meal_plan_snack_DTOs = [
                Extended_Meal_Plan_Snack_DTO(extended_meal_plan_snack_domain=x)
                for x in extended_meal_plan_snacks
            ]
            food_nutrient_stats_dtos: list[Food_Nutrient_Stats_DTO] = []
            for meal_plan_snack_dto in extended_meal_plan_snack_DTOs:
                food_nutrient_stats_dtos.append(
                    Food_Nutrient_Stats_Service().extract_nutrient_stats(
                        extended_meal_plan_food=meal_plan_snack_dto
                    )
                )
            serialized_food_nutrient_stats_dtos = [
                x.serialize() for x in food_nutrient_stats_dtos
            ]
            return jsonify(serialized_food_nutrient_stats_dtos), 200

    else:
        return Response(status=405)


@app.route("/api/nysand_lead", methods=["POST"])
def nysand_lead() -> Response:
    if request.method == "POST":
        from repository.NYSAND_Lead_Repository import NYSAND_Lead_Repository

        dietitian_id = json.loads(request.data)["dietitian_id"]
        NYSAND_Lead_Repository(db=db).create_nysand_lead(dietitian_id=dietitian_id)
        return Response(status=200)
    else:
        return Response(status=405)


@app.route("/api/dietitian/initialize", methods=["GET"])
def initialize_dietitian() -> Response:
    if request.method == "GET":
        from repository.Dietitian_Repository import Dietitian_Repository
        from repository.Continuity_Repository import Continuity_Repository
        from repository.Meal_Sample_Repository import Meal_Sample_Repository
        from repository.Meal_Sample_Shipment_Repository import (
            Meal_Sample_Shipment_Repository,
        )
        from service.Dietitian_Service import Dietitian_Service
        from service.Continuity_Service import Continuity_Service
        from service.Meal_Sample_Service import Meal_Sample_Service
        from service.Meal_Sample_Shipment_Service import Meal_Sample_Shipment_Service

        Dietitian_Service(
            dietitian_repository=Dietitian_Repository(db=db)
        ).initialize_dietitians()
        dietitians = Dietitian_Service(
            dietitian_repository=Dietitian_Repository(db=db)
        ).get_dietitians()
        dietitian_dict = {}
        for dietitian in dietitians:
            dietitian_dict[dietitian.email] = dietitian.serialize()
        Continuity_Repository().initialize_dietitian_data(
            dietitian_dict=dietitian_dict,
            meal_sample_repository=Meal_Sample_Repository(db=db),
            meal_sample_shipment_repository=Meal_Sample_Shipment_Repository(db=db),
        )
        return Response(status=200)
    else:
        return Response(status=405)


if env == "debug":
    debug = True
else:
    debug = False

PORT = os.environ.get("PORT", 4000)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=debug)
