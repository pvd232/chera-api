from domain.Dietitian_Domain import Dietitian_Domain
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from repository.Dietitian_Repository import Dietitian_Repository
    from dto.Dietitian_DTO import Dietitian_DTO


class Dietitian_Service(object):
    def __init__(self, dietitian_repository: "Dietitian_Repository") -> None:
        self.dietitian_repository = dietitian_repository

    def get_dietitians(self) -> list[Dietitian_Domain]:
        dietitian_domains: list[Dietitian_Domain] = [
            Dietitian_Domain(dietitian_object=x)
            for x in self.dietitian_repository.get_dietitians()
        ]
        return dietitian_domains

    def get_dietitian(self, dietitian_email: str) -> Optional[Dietitian_Domain]:
        requested_dietitian = self.dietitian_repository.get_dietitian(
            dietitian_email=dietitian_email
        )
        if requested_dietitian:
            return Dietitian_Domain(dietitian_object=requested_dietitian)
        else:
            return None

    def create_dietitian(self, dietitian_dto: "Dietitian_DTO") -> Dietitian_Domain:
        requested_dietitian_domain = Dietitian_Domain(dietitian_object=dietitian_dto)
        created_dietitian = self.dietitian_repository.create_dietitian(
            dietitian=requested_dietitian_domain
        )
        created_dietitian_domain = Dietitian_Domain(dietitian_object=created_dietitian)
        return created_dietitian_domain

    def initialize_dietitians(self) -> None:
        self.dietitian_repository.initialize_dietitians()
        return

    def delete_dietitian(self, dietitian_email: str) -> None:
        self.dietitian_repository.delete_dietitian(dietitian_email=dietitian_email)
        return
