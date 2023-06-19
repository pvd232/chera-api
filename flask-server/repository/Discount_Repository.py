from repository.Base_Repository import Base_Repository
from models import Discount_Model
from typing import Optional


class Discount_Repository(Base_Repository):
    def get_discounts(self) -> list[Discount_Model]:
        discounts = self.db.session.query(Discount_Model).all()
        return discounts

    def get_discount(self, discount_code: str) -> Discount_Model:
        requested_discount = (
            self.db.session.query(Discount_Model)
            .filter(Discount_Model.code == discount_code)
            .first()
        )
        return requested_discount

    def verify_discount(self, discount_code: str) -> Optional[Discount_Model]:
        requested_discount = (
            self.db.session.query(Discount_Model)
            .filter(Discount_Model.code == discount_code)
            .first()
        )
        if requested_discount:
            return requested_discount
        else:
            return None

    def initialize_discounts(self) -> None:
        from pathlib import Path
        from utils.load_json import load_json
        from domain.Discount_Domain import Discount_Domain
        from dto.Discount_DTO import Discount_DTO

        discount_json_file = Path(".", "nutrient_data", "new_discounts.json")
        discounts_data = load_json(filename=discount_json_file)

        # Only initialize custom values, not USDA values which are initialized alongside Discount_Models
        for discount_json in discounts_data:
            discount_dto = Discount_DTO(discount_json=discount_json)
            discount_domain = Discount_Domain(discount_object=discount_dto)

            new_discount_model = Discount_Model(discount_domain=discount_domain)
            self.db.session.add(new_discount_model)
        self.db.session.commit()
