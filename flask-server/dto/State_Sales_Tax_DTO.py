from .Base_DTO import Base_DTO
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from domain import State_Sales_Tax_Domain


class State_Sales_Tax_DTO(Base_DTO):
    def __init__(self, state_sales_tax_domain: 'State_Sales_Tax_Domain') -> None:
        self.state: str = state_sales_tax_domain.state
        self.sales_tax_percentage: float = state_sales_tax_domain.sales_tax_percentage
        self.stripe_tax_id: str = state_sales_tax_domain.stripe_tax_id
