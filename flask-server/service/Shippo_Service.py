import shippo
from uuid import uuid4 as uuid
from typing import Optional, TYPE_CHECKING
from domain.Meal_Shipment_Domain import Meal_Shipment_Domain

if TYPE_CHECKING:
    from models import Meal_Shipment_Model
    from domain.Client_Domain import Client_Domain
    from repository.Meal_Shipment_Repository import Meal_Shipment_Repository


class Shippo_Service(object):
    def __init__(self):
        self.address_from : dict[str, str] = {
            "name": "Peter Driscoll",
            "street1": "922 E 49th St",
            "city": "Austin",
            "state": "TX",
            "zip": "78751",
            "country": "US",
        }
        self.four_meals_parcel: dict = {
            'length':   12,
            'width':    9,
            'height':   4.5,
            'weight': 10,
            'distance_unit': "in",
            'mass_unit': "lb",
        }
        self.six_meals_parcel: dict = {
            'length':   12,
            'width':    9,
            'height':   7,
            'weight': 10,
            'distance_unit': "in",
            'mass_unit': "lb",
        }

    def create_shipment(
        self,
        meal_subscription_invoice_id: str,
        client: "Client_Domain",
        meal_shipment_repository: "Meal_Shipment_Repository",
    ) -> Optional["Meal_Shipment_Model"]:
        client_name: str = f"{client.first_name} {client.last_name}"
        if client.suite != "":
            address_to = {
                "name": client_name,
                "street1": client.street,
                "street2": client.suite,
                "city": client.city,
                "state": client.state,
                "zip": client.zipcode + "-" + client.zipcode_extension,
                "email": client.id,
                "country": "US",
            }
        else:
            address_to = {
                "name": client_name,
                "street1": client.street,
                "city": client.city,
                "state": client.state,
                "zip": client.zipcode + "-" + client.zipcode_extension,
                "country": "US",
            }

        # update to cubic
        parcel = shippo.Parcel.create(
            length=12,
            width=9,
            height=7,
            distance_unit="in",
            mass_unit="lb",
            weight="10",
        )

        shipment = shippo.Shipment.create(
            address_from    = self.address_from,
            address_to      = address_to,
            parcels         = parcel,
            asynchronous    = False,
        )

        # USPS rates are listed 1. priority express /overnight 2. priority 2 day 3. ground
        rate = shipment.rates[1]

        # Purchase the desired rate.
        transaction = shippo.Transaction.create(
            rate=rate.object_id, label_file_type="PDF", asynchronous=False
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
            print(transaction.messages)
    
    # get estimate shippingcost
    def get_shipping_costs(self, zip_code):
        def shipping_cost(parcel):
            shipment = shippo.Shipment.create(
                address_from    = self.address_from,
                address_to      = {'zip': zip_code, 'country' : 'US'},
                parcels         = [parcel],
                asynchronous    = False
            )
        
            rates = shipment.rates
            if rates:
                return float(rates[1].amount)
            else:
                return 0
        costs : dict[str, float] = {
            'four_meals': shipping_cost(self.four_meals_parcel),
            'six_meals': shipping_cost(self.six_meals_parcel)
        }
        return costs

