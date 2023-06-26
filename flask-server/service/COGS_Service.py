from domain.COGS_Domain import COGS_Domain
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from repository.COGS_Repository import COGS_Repository


class COGS_Service(object):
    def __init__(self, cogs_repository: "COGS_Repository") -> None:
        self.cogs_repository = cogs_repository

    def get_cogs(self) -> list[COGS_Domain]:
        return self.cogs_repository.get_cogs()

    def get_specific_cogs(self, num_meals: int, is_local: bool) -> COGS_Domain:
        return COGS_Domain(
            cogs_object=self.cogs_repository.get_cogs(
                num_meals=num_meals, is_local=is_local
            )
        )
