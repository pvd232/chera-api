from .Client_Service import Client_Service
from domain.Extended_Client_Domain import Extended_Client_Domain
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from models import Client_Model


class Extended_Client_Service(Client_Service):
    def get_extended_clients(self, dietitian_id: str) -> Optional[list['Extended_Client_Domain']]:
        clients: Optional[list['Client_Model']] = self.client_repository.get_clients(
            dietitian_id=dietitian_id)
        if clients:
            return [Extended_Client_Domain(client_model=x) for x in clients]
        else:
            return None
