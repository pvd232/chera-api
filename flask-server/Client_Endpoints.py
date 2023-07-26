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
from flask_restplus import Namespace, Resource
#Importing other required moduels 
from service.Client_Service import Client_Service
from service.Email_Service import Email_Service
from service.GCP_Secret_Manager_Service import GCP_Secret_Manager_Service
from repository.Client_Repository import Client_Repository
from domain.Client_Domain import Client_Domain
from dto.Client_DTO import Client_DTO
#Define your Flask RestPlus API namespace
api = Namespace('client', description='Client related operations')


@app.route("/api/client")
def Client(Resource):
    @api.response(200, "Client list retrieved successfully")
    @api.response(405, "Method not allowed")
    def get(self):
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

    @api.response(201, "Client created successfully")
    @api.response(405, "Method not allowed")
    def post(self):
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
            email="patardriscoll@gmail.com",
            user_type="Client",
            user=returned_client,
            env=env,
            zipcode=returned_client.zipcode,
        )
        returned_client_dto = Client_DTO(client_domain=returned_client)

        return jsonify(returned_client_dto.serialize()), 201
    
    @api.response(200, "Client meal plan updated successfully")
    @api.response(405, "Method not allowed")
    def put(self):
        client_dto: Client_DTO = Client_DTO(client_json=json.loads(request.data))
        Client_Service(
            client_repository=Client_Repository(db=db)
        ).update_client_meal_plan(client_dto=client_dto)
        return Response(status=200)


