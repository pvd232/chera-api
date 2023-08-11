from models import COGS_Model
from domain.COGS_Domain import COGS_Domain
from dto.COGS_DTO import COGS_DTO
from flask_sqlalchemy import SQLAlchemy


def create_cogs(db: SQLAlchemy) -> None:
    costs = [
        {
            "num_meals": 6,
            "ingredient": 3,
            "core_packaging": 0.459,
            "kitchen": 1.3,
            "chef": 0,
            "box": 2.120,
            "ice": 0.507,
            "num_boxes": 1,
            "is_local": False,
        },
        {
            "num_meals": 7,
            "ingredient": 3,
            "core_packaging": 0.459,
            "kitchen": 1.3,
            "chef": 0,
            "box": 1.817,
            "ice": 0.434,
            "num_boxes": 1,
            "is_local": False,
        },
        {
            "num_meals": 8,
            "ingredient": 3,
            "core_packaging": 0.459,
            "kitchen": 1.3,
            "chef": 0,
            "box": 1.590,
            "ice": 0.38,
            "num_boxes": 1,
            "is_local": False,
        },
        {
            "num_meals": 9,
            "ingredient": 3,
            "core_packaging": 0.459,
            "kitchen": 1.3,
            "chef": 0,
            "box": 2.827,
            "ice": 0.676,
            "num_boxes": 1,
            "is_local": False,
        },
        {
            "num_meals": 10,
            "ingredient": 3,
            "core_packaging": 0.459,
            "kitchen": 1.3,
            "chef": 0,
            "box": 2.544,
            "ice": 0.608,
            "num_boxes": 2,
            "is_local": False,
        },
        {
            "num_meals": 11,
            "ingredient": 3,
            "core_packaging": 0.459,
            "kitchen": 1.3,
            "chef": 0,
            "box": 2.313,
            "ice": 0.507,
            "num_boxes": 2,
            "is_local": False,
        },
        {
            "num_meals": 12,
            "ingredient": 3,
            "core_packaging": 0.459,
            "kitchen": 1.3,
            "chef": 0,
            "box": 1.957,
            "ice": 0.468,
            "num_boxes": 2,
            "is_local": False,
        },
        {
            "num_meals": 13,
            "ingredient": 3,
            "core_packaging": 0.459,
            "kitchen": 1.3,
            "chef": 0,
            "box": 1.817,
            "ice": 0.434,
            "num_boxes": 2,
            "is_local": False,
        },
        {
            "num_meals": 14,
            "ingredient": 3,
            "core_packaging": 0.459,
            "kitchen": 1.3,
            "chef": 0,
            "box": 1.696,
            "ice": 0.405,
            "num_boxes": 2,
            "is_local": False,
        },
        {
            "num_meals": 15,
            "ingredient": 3,
            "core_packaging": 0.459,
            "kitchen": 1.3,
            "chef": 0,
            "box": 1.696,
            "ice": 0.405,
            "num_boxes": 2,
            "is_local": False,
        },
    ]
    for cost in costs:
        cogs_dto = COGS_DTO(cogs_json=cost)
        cogs_domain = COGS_Domain(cogs_object=cogs_dto)
        cogs_model = COGS_Model(cogs_domain=cogs_domain)
        db.session.add(cogs_model)
    db.session.commit()
