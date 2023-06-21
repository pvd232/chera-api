from domain.Dietary_Restriction_Domain import Dietary_Restriction_Domain
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from repository.Dietary_Restriction_Repository import Dietary_Restriction_Repository


class Dietary_Restriction_Service(object):
    def __init__(
        self, dietary_restriction_repository: "Dietary_Restriction_Repository"
    ) -> None:
        self.dietary_restriction_repository = dietary_restriction_repository

    def get_dietary_restrictions(self) -> list[Dietary_Restriction_Domain]:
        dietary_restriction_models = (
            self.dietary_restriction_repository.get_dietary_restrictions()
        )
        dietary_restriction_domains = [
            Dietary_Restriction_Domain(dietary_restriction_object=x)
            for x in dietary_restriction_models
        ]
        return dietary_restriction_domains

    def write_dietary_restrictions(self) -> None:
        from pathlib import Path
        from utils.write_json import write_json

        dietary_restriction_json_file = Path(
            ".", "nutrient_data", "new_dietary_restrictions.json"
        )
        with open(dietary_restriction_json_file, "r+") as outfile:
            dietary_restriction_dicts = [
                x.serialize() for x in self.get_dietary_restrictions()
            ]
            write_json(outfile=outfile, dicts=dietary_restriction_dicts)
