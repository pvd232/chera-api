from .Base_Domain import Base_Domain
from models import State_Sales_Tax_Model
from dto.State_Sales_Tax_DTO import State_Sales_Tax_DTO


class State_Sales_Tax_Domain(Base_Domain):
    def __init__(self, state_sales_tax_object: State_Sales_Tax_Model | State_Sales_Tax_DTO) -> None:
        self.state = state_sales_tax_object.state
        self.sales_tax_percentage = state_sales_tax_object.sales_tax_percentage
        self.stripe_tax_id = state_sales_tax_object.stripe_tax_id
