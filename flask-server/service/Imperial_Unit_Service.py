from typing import TYPE_CHECKING
from domain.Imperial_Unit_Domain import Imperial_Unit_Domain

if TYPE_CHECKING:
    from repository.Imperial_Unit_Repository import Imperial_Unit_Repository


class Imperial_Unit_Service:
    def __init__(self, imperial_unit_repository: "Imperial_Unit_Repository") -> None:
        self.imperial_unit_repository = imperial_unit_repository

    def get_imperial_units(self) -> list[Imperial_Unit_Domain]:
        imperial_units = self.imperial_unit_repository.get_imperial_units()
        imperial_unit_domains = [
            Imperial_Unit_Domain(imperial_unit_object=x) for x in imperial_units
        ]
        return imperial_unit_domains

    def write_imperial_units(self) -> None:
        from pathlib import Path
        from utils.write_json import write_json

        imperial_unit_json_file = Path(".", "nutrient_data", "new_imperial_units.json")
        with open(imperial_unit_json_file, "r+") as outfile:
            imperial_unit_dicts = [x.serialize() for x in self.get_imperial_units()]
            write_json(outfile=outfile, dicts=imperial_unit_dicts)
