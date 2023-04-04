from typing import TYPE_CHECKING
from domain.Imperial_Unit_Domain import Imperial_Unit_Domain
if TYPE_CHECKING:
    from repository.Imperial_Unit_Repository import Imperial_Unit_Repository


class Imperial_Unit_Service():
    def __init__(self, imperial_unit_repository: 'Imperial_Unit_Repository') -> None:
        self.imperial_unit_repository = imperial_unit_repository

    def get_imperial_units(self) -> list[Imperial_Unit_Domain]:
        imperial_units = self.imperial_unit_repository.get_imperial_units()
        imperial_unit_domains = [Imperial_Unit_Domain(
            imperial_unit_object=x) for x in imperial_units]
        return imperial_unit_domains
