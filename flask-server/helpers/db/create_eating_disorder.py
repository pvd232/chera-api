from models import Eating_Disorder_Model
from domain.Eating_Disorder_Domain import Eating_Disorder_Domain
from dto.Eating_Disorder_DTO import Eating_Disorder_DTO
from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4

def create_eating_disorder(db: SQLAlchemy) -> None:
    disorders = [
        {
            "id": uuid4(),
            "name": "Anorexia nervosa"
        },
        {
            "id": uuid4(),
            "name": "Binge eating disorder"
        },
                {
            "id": uuid4(),
            "name": "Other Specified Feeding and Eating Disorders"
        },
        {
            "id": uuid4(),
            "name": "Avoidant Restrictive Food Intake Disorder"
        },
        {
        "id": uuid4(),
            "name": "Rumination disorder"
        },
        {
            "id": uuid4(),
            "name": "Unspecified feeding or eating disorder"
        },
    ]
    for disorder in disorders:
        eating_disorder_dto = Eating_Disorder_DTO(eating_disorder_json=disorder)
        eating_disorder_domain = Eating_Disorder_Domain(eating_disorder_object=eating_disorder_dto)
        eating_disorder_model = Eating_Disorder_Model(eating_disorder_domain=eating_disorder_domain)
        db.session.add(eating_disorder_model)
    db.session.commit()
