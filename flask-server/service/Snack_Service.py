from domain.Snack_Domain import Snack_Domain
from uuid import UUID
import json
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from repository.Snack_Repository import Snack_Repository
    from dto.Snack_DTO import Snack_DTO


class Snack_Service(object):
    def __init__(self, snack_repository: "Snack_Repository") -> None:
        self.snack_repository = snack_repository

    def get_snacks(self) -> list[Snack_Domain]:
        snack_domains: list[Snack_Domain] = [
            Snack_Domain(snack_object=x) for x in self.snack_repository.get_snacks()
        ]
        return snack_domains

    def get_snack(self, snack_id: UUID) -> Optional[Snack_Domain]:
        requested_snack_domain = self.snack_repository.get_snack(snack_id=snack_id)
        if requested_snack_domain:
            snack_domain = Snack_Domain(snack_object=requested_snack_domain)
        return snack_domain

    def create_snack(self, snack_dto: "Snack_DTO") -> None:
        snack_domain = Snack_Domain(snack_object=snack_dto)
        self.snack_repository.create_snack(snack_domain=snack_domain)
        return

    # NO matching JSON file for this method yet
    def write_snacks(self) -> None:
        with open("new_snacks.json", "r+") as outfile:
            snack_dtos = [x.serialize() for x in self.get_snacks()]
            data = json.load(outfile)
            if data:
                outfile.seek(0)
                json.dump(snack_dtos, outfile, indent=4)
                outfile.truncate()
            else:
                outfile.write(json.dumps(snack_dtos, indent=4))
