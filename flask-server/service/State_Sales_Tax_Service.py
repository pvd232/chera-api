from models import State_Sales_Tax_Model
from domain.State_Sales_Tax_Domain import State_Sales_Tax_Domain
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from repository.State_Sales_Tax_Repository import State_Sales_Tax_Repository


class State_Sales_Tax_Service(object):
    def __init__(self, state_sales_tax_repository: 'State_Sales_Tax_Repository') -> None:
        self.state_sales_tax_repository = state_sales_tax_repository

    def get_sales_tax(self, state: str) -> State_Sales_Tax_Model:
        return State_Sales_Tax_Domain(state_sales_tax_object=self.state_sales_tax_repository.get_sales_tax(state=state))
