from domain.Eating_Disorder_Domain import Eating_Disorder_Domain
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from repository.Eating_Disorder_Repository import Eating_Disorder_Repository


class Eating_Disorder_Service(object):
    def __init__(
        self, eating_disorder_repository: "Eating_Disorder_Repository"
    ) -> None:
        self.eating_disorder_repository = eating_disorder_repository

    def get_eating_disorders(self) -> list[Eating_Disorder_Domain]:
        eating_disorder_models = (
            self.eating_disorder_repository.get_eating_disorders()
        )
        eating_disorder_domains = [
            Eating_Disorder_Domain(eating_disorder_object=x)
            for x in eating_disorder_models
        ]
        return eating_disorder_domains
