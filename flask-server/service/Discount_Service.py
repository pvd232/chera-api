from domain.Discount_Domain import Discount_Domain
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from repository.Discount_Repository import Discount_Repository


class Discount_Service(object):
    def __init__(self, discount_repository: "Discount_Repository") -> None:
        self.discount_repository = discount_repository

    def get_discounts(self) -> list[Discount_Domain]:
        discount_domains = [
            Discount_Domain(discount_object=x)
            for x in self.discount_repository.get_discounts()
        ]
        return discount_domains

    def get_discount(self, discount_code: str) -> Discount_Domain:
        discount = self.discount_repository.get_discount(discount_code=discount_code)
        return Discount_Domain(discount_object=discount)

    def verify_discount_code(self, discount_code: str) -> Optional[Discount_Domain]:
        discount_code = self.discount_repository.verify_discount(
            discount_code=discount_code
        )
        if discount_code:
            return Discount_Domain(discount_object=discount_code)
        else:
            return None

    def write_discounts(self) -> None:
        from pathlib import Path
        from utils.write_json import write_json

        discount_json_file = Path(".", "nutrient_data", "new_discounts.json")
        with open(discount_json_file, "r+") as outfile:
            discount_dicts = [x.serialize() for x in self.get_discounts()]
            write_json(outfile=outfile, dicts=discount_dicts)
