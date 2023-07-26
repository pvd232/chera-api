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
from flask_restplus import Api, Resource
# Importing other required modules
from service.Staged_Client_Service import Staged_Client_Service
from service.Email_Service import Email_Service
from service.GCP_Secret_Manager_Service import GCP_Secret_Manager_Service
from repository.Staged_Client_Repository import Staged_Client_Repository
from domain.Staged_Client_Domain import Staged_Client_Domain
from dto.Staged_Client_DTO import Staged_Client_DTO

# Define your Flask RestPlus API namespace
api = Api(app, title="Staged Client API", description="API for Staged Clients")


@app.route("/api/staged_client/<string:staged_client_id>")
class StagedClientById(Resource):
    @api.response(200, "Staged Client retrieved successfully")
    @api.response(404, "Staged Client not found")
    def get(self, staged_client_id: str):
        staged_client: Optional[Staged_Client_Domain] = Staged_Client_Service(
            staged_client_repository=Staged_Client_Repository(db=db)
        ).get_staged_client(staged_client_id=staged_client_id)

        # Username is unavailable
        if staged_client:
            staged_client_dto = Staged_Client_DTO(staged_client_domain=staged_client)
            return jsonify(staged_client_dto.serialize()), 200
        # Username is available
        else:
            return Response(status=404)
    
@app.route(
    "/api/staged_client",
    defaults={"staged_client_id": None}
)
class StagedClient(Resource):
    @api.response(200, "List of staged clients retrieved successfully")
    @api.response(405, "Method not allowed")
    def get(self):
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

    @api.response(201, "Staged client created successfully")
    @api.response(405, "Method not allowed")    
    def post(self):
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
            email="patardriscoll@gmail.com",
            user_type="Staged_Client",
            user=new_staged_client_domain,
            env=env,
            zipcode=None,
        )
        return Response(status=201)

    @api.response(204, "Staged client meal plan updated successfully")
    @api.response(405, "Method not allowed")
    def put(self):
        staged_client_dto: Staged_Client_DTO = Staged_Client_DTO(
                staged_client_json=json.loads(request.data)
            )
        Staged_Client_Service(
                staged_client_repository=Staged_Client_Repository(db=db)
            ).update_staged_client_meal_plan(staged_client_dto=staged_client_dto)
        return Response(status=204)





