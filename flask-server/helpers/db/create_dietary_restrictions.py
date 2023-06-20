from flask_sqlalchemy import SQLAlchemy
from models import Dietary_Restriction_Model


def create_dietary_restrictions(db: SQLAlchemy) -> None:
    dietary_restrictions = ["vegetarian"]
    for dietary_restriction in dietary_restrictions:
        new_dietary_restriction = Dietary_Restriction_Model(id=dietary_restriction)
        db.session.add(new_dietary_restriction)
    db.session.commit()
