from models import app, db, env, host_url, oauth
from flask import (
    Response,
    request,
    jsonify,
)
import json
from werkzeug.exceptions import HTTPException
from typing import Optional
import uuid
from flask_restplus import Resource, Api, fields
#Import other required modules
from repository.Meal_Repository import Meal_Repository
from repository.Meal_Sample_Repository import Meal_Sample_Repository
from service.Dietitian_Service import Dietitian_Service
from service.Email_Service import Email_Service
from service.GCP_Secret_Manager_Service import GCP_Secret_Manager_Service
from service.Meal_Service import Meal_Service
from service.Meal_Sample_Service import Meal_Sample_Service
from service.Shippo_Service import Shippo_Service
from repository.Dietitian_Repository import Dietitian_Repository
from dto.Dietitian_DTO import Dietitian_DTO
from dto.Meal_Sample_DTO import Meal_Sample_DTO

# Define your Flask RestPlus API namespace
api = Api(app, title="Dietitian API", description="API for Dietitians")

@app.route("/api/dietitian")
class Dietician(Resource):
    @api.response(201, "Dietitian created successfully")
    @api.response(405, "Method not allowed")
    def post(self):
        requested_dietitian = json.loads(request.data)
        requested_dietitian_dto = Dietitian_DTO(
            gcp_secret_manager_service=GCP_Secret_Manager_Service(),
            dietitian_json=requested_dietitian,
        )
        created_dietitian_domain = Dietitian_Service(
            dietitian_repository=Dietitian_Repository(db=db)
        ).create_dietitian(dietitian_dto=requested_dietitian_dto)
        Email_Service(
            gcp_secret_manager_service=GCP_Secret_Manager_Service(),
        ).send_confirmation_email(user_type="Dietitian", user=created_dietitian_domain)
        if created_dietitian_domain.got_sample:
            # shipping_address =
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
            email="patardriscoll@gmail.com",
            user_type="Dietitian",
            user=created_dietitian_domain,
            env=env,
        )

        dietitian_dto = Dietitian_DTO(
            gcp_secret_manager_service=GCP_Secret_Manager_Service(),
            dietitian_domain=created_dietitian_domain,
        )
        serialized_dietitian_dto = dietitian_dto.serialize()
        return jsonify(serialized_dietitian_dto), 201

            