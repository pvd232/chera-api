import shippo
from uuid import uuid4 as uuid
from typing import Optional, TYPE_CHECKING
from domain.Meal_Shipment_Domain import Meal_Shipment_Domain
from domain.Meal_Sample_Shipment_Domain import Meal_Sample_Shipment_Domain

if TYPE_CHECKING:
    from models import Meal_Shipment_Model
    from models import Meal_Sample_Shipment_Model
    from domain.Client_Domain import Client_Domain
    from domain.Dietitian_Domain import Dietitian_Domain
    from repository.Meal_Shipment_Repository import Meal_Shipment_Repository
    from repository.Meal_Sample_Shipment_Repository import (
        Meal_Sample_Shipment_Repository,
    )


class Shippo_Service(object):
    def __init__(
        self,
        address_from: dict[str, str] = None,
        standard_parcel: dict[str, str] = None,
        sample_parcel: dict[str, str] = None,
    ) -> None:
        if address_from:
            self.address_from = address_from
        else:
            self.address_from = {
                "name": "Peter Driscoll",
                "street1": "525 hopkins ln",
                "city": "Haddonfield",
                "state": "NJ",
                "zip": "08033-1128",
                "country": "US",
            }
        if standard_parcel:
            self.standard_parcel = standard_parcel
        else:
            self.standard_parcel = {
                "length": 12,
                "width": 9,
                "height": 8,
                "weight": 15,
            }
        if sample_parcel:
            self.sample_parcel = sample_parcel
        else:
            self.sample_parcel = {
                "length": 7,
                "width": 5,
                "height": 4,
                "weight": 5,
            }
        self.distance_unit = "in"
        self.mass_unit = "lb"

    def get_shipping_rate(self, zipcode: str) -> float:
        address_to = {
            "zip": zipcode,
            "country": "US",
        }
        shippo_parcel = shippo.Parcel.create(
            length=self.standard_parcel["length"],
            width=self.standard_parcel["width"],
            height=self.standard_parcel["height"],
            distance_unit=self.distance_unit,
            mass_unit=self.mass_unit,
            weight=self.standard_parcel["weight"],
        )

        meal_shipment = shippo.Shipment.create(
            address_from=self.address_from,
            address_to=address_to,
            parcels=shippo_parcel,
            asynchronous=False,
        )

        shipment_rates = shippo.Shipment.get_rates(meal_shipment.object_id)["results"]

        for rate in shipment_rates:
            if rate["servicelevel"]["token"] == "usps_priority":
                shipment_rate = rate
                break

        return float(shipment_rate["amount"])

    def create_shipment(
        self,
        meal_subscription_invoice_id: str,
        client: "Client_Domain",
        meal_shipment_repository: "Meal_Shipment_Repository",
    ) -> Optional["Meal_Shipment_Model"]:
        client_name: str = f"{client.first_name} {client.last_name}"
        address_to = {
            "name": client_name,
            "street1": client.street,
            "city": client.city,
            "state": client.state,
            "zip": client.zipcode + "-" + client.zipcode_extension,
            "country": "US",
        }
        if client.suite != "":
            address_to["suite"] = client.suite
        # update to cubic
        parcel = shippo.Parcel.create(
            length=self.standard_parcel["length"],
            width=self.standard_parcel["width"],
            height=self.standard_parcel["height"],
            distance_unit=self.distance_unit,
            mass_unit=self.mass_unit,
            weight=self.standard_parcel["weight"],
        )

        shipment = shippo.Shipment.create(
            address_from=self.address_from,
            address_to=address_to,
            parcels=parcel,
            asynchronous=False,
        )

        for rate in shipment.rates:
            if rate["servicelevel"]["token"] == "usps_priority":
                shipment_rate = rate
                break
        # Purchase the desired rate.
        transaction = shippo.Transaction.create(
            rate=shipment_rate.object_id, label_file_type="PDF", asynchronous=False
        )

        # Retrieve label url and tracking number
        if transaction.status == "SUCCESS":
            # create new shipment object with tracking number and label url
            meal_shipment_dict = {
                "id": uuid(),
                "meal_subscription_invoice_id": meal_subscription_invoice_id,
                "shippo_transaction_id": transaction.object_id,
                "label_url": transaction.label_url,
                "tracking_number": str(transaction.tracking_number),
                "tracking_url": transaction.tracking_url_provider,
            }
            meal_shipment_domain = Meal_Shipment_Domain(
                meal_shipment_json=meal_shipment_dict
            )
            meal_shipment_repository.create_shipment(meal_shipment=meal_shipment_domain)
            return meal_shipment_domain
        else:
            print("transaction failed, printing messages", transaction.messages)

    def create_sample_shipment(
        self,
        dietitian: "Dietitian_Domain",
        shipping_address: dict[str, str],
        meal_sample_shipment_repository: "Meal_Sample_Shipment_Repository",
    ) -> Optional["Meal_Sample_Shipment_Model"]:
        dietitian_name: str = f"{dietitian.first_name} {dietitian.last_name}"
        address_to = {
            "name": dietitian_name,
            "street1": shipping_address["street"],
            "city": shipping_address["city"],
            "state": shipping_address["state"],
            "zip": shipping_address["zipcode"],
            "country": "US",
        }
        if shipping_address["suite"] != "":
            address_to["suite"] = shipping_address["suite"]
        # update to cubic
        parcel = shippo.Parcel.create(
            length=self.sample_parcel["length"],
            width=self.sample_parcel["width"],
            height=self.sample_parcel["height"],
            distance_unit=self.distance_unit,
            mass_unit=self.mass_unit,
            weight=self.sample_parcel["weight"],
        )

        shipment = shippo.Shipment.create(
            address_from=self.address_from,
            address_to=address_to,
            parcels=parcel,
            asynchronous=False,
        )

        # USPS rates are listed 1. priority express /overnight 2. priority 2 day 3. ground
        for rate in shipment.rates:
            if rate["servicelevel"]["token"] == "usps_priority":
                shipment_rate = rate
                break
        # Purchase the desired rate.
        transaction = shippo.Transaction.create(
            rate=shipment_rate.object_id, label_file_type="PDF", asynchronous=False
        )

        # Retrieve label url and tracking number
        if transaction.status == "SUCCESS":
            # create new shipment object with tracking number and label url
            meal_sample_shipment_dict = {
                "id": uuid(),
                "dietitian_id": dietitian.id,
                "shippo_transaction_id": transaction.object_id,
                "label_url": transaction.label_url,
                "tracking_number": str(transaction.tracking_number),
                "tracking_url": transaction.tracking_url_provider,
            }
            meal_sample_shipment_domain = Meal_Sample_Shipment_Domain(
                meal_sample_shipment_json=meal_sample_shipment_dict
            )
            meal_sample_shipment_repository.create_shipment(
                meal_sample_shipment=meal_sample_shipment_domain
            )
            return meal_sample_shipment_domain
        else:
            print("transaction failed, printing messages", transaction.messages)
