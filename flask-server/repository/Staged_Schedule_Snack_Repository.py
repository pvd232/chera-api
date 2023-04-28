from repository.Base_Repository import Base_Repository
from models import Staged_Schedule_Snack_Model
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from domain.Staged_Schedule_Snack_Domain import Staged_Schedule_Snack_Domain


class Staged_Schedule_Snack_Repository(Base_Repository):
    def create_staged_schedule_snacks(
        self, staged_schedule_snack_domains: list["Staged_Schedule_Snack_Domain"]
    ) -> None:
        for staged_schedule_snack_domain in staged_schedule_snack_domains:
            new_staged_schedule_snack = Staged_Schedule_Snack_Model(
                staged_schedule_snack_domain=staged_schedule_snack_domain
            )
            self.db.session.add(new_staged_schedule_snack)
        self.db.session.commit()
        return

    def get_staged_schedule_snacks(
        self, staged_client_id: str
    ) -> Optional[list[Staged_Schedule_Snack_Model]]:
        staged_schedule_snacks = (
            self.db.session.query(Staged_Schedule_Snack_Model)
            .filter(Staged_Schedule_Snack_Model.staged_client_id == staged_client_id)
            .all()
        )
        return staged_schedule_snacks
