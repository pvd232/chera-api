from .Staged_Client_Service import Staged_Client_Service
from domain.Extended_Staged_Client_Domain import Extended_Staged_Client_Domain
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from models import Staged_Client_Model


class Extended_Staged_Client_Service(Staged_Client_Service):
    def get_extended_staged_clients(self, dietitian_id: str) -> Optional[list['Extended_Staged_Client_Domain']]:
        staged_clients: Optional[list['Staged_Client_Model']] = self.staged_client_repository.get_staged_clients(
            dietitian_id=dietitian_id)
        if staged_clients:
            return [Extended_Staged_Client_Domain(staged_client_model=x) for x in staged_clients]
        else:
            return None
