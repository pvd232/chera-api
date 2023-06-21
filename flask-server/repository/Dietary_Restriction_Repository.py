from .Base_Repository import Base_Repository
from models import Dietary_Restriction_Model


class Dietary_Restriction_Repository(Base_Repository):
    def get_dietary_restrictions(self) -> list[Dietary_Restriction_Model]:
        return self.db.session.query(Dietary_Restriction_Model).all()

    def initialize_dietary_restrictions(self) -> None:
        from pathlib import Path
        from utils.load_json import load_json
        from domain.Dietary_Restriction_Domain import Dietary_Restriction_Domain
        from dto.Dietary_Restriction_DTO import Dietary_Restriction_DTO

        dietary_restriction_json_file = Path(
            ".", "nutrient_data", "new_dietary_restrictions.json"
        )
        dietary_restrictions_data = load_json(filename=dietary_restriction_json_file)

        for dietary_restriction_json in dietary_restrictions_data:
            dietary_restriction_dto = Dietary_Restriction_DTO(
                dietary_restriction_json=dietary_restriction_json
            )
            dietary_restriction_domain = Dietary_Restriction_Domain(
                dietary_restriction_object=dietary_restriction_dto
            )

            dietary_restriction_model = Dietary_Restriction_Model(
                dietary_restriction_domain=dietary_restriction_domain
            )
            self.db.session.add(dietary_restriction_model)
        self.db.session.commit()
