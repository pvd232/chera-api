from repository.Base_Repository import Base_Repository
from models import State_Sales_Tax_Model
from typing import Optional


class State_Sales_Tax_Repository(Base_Repository):
    def get_sales_tax(self, state: str) -> Optional[State_Sales_Tax_Model]:
        sales_tax = self.db.session.query(State_Sales_Tax_Model).filter(
            State_Sales_Tax_Model.state == state).first()
        return sales_tax
