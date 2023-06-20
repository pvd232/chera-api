from flask_sqlalchemy import SQLAlchemy
from models import USDA_Ingredient_Model, USDA_Ingredient_Nutrient_Model


def wipe_all_usda_ingredient_related_data(
    db: SQLAlchemy, usda_ingredient_id: str
) -> None:
    usda_ingredient = (
        db.session.query(USDA_Ingredient_Model)
        .filter(USDA_Ingredient_Model.id == usda_ingredient_id)
        .first()
    )
    nutrients = (
        db.session.query(USDA_Ingredient_Nutrient_Model)
        .filter(USDA_Ingredient_Nutrient_Model.usda_ingredient_id == usda_ingredient.id)
        .all()
    )
    for usda_ingredient_nutrient in nutrients:
        db.session.delete(usda_ingredient_nutrient)
    for usda_ingredient_portion in usda_ingredient.portions:
        db.session.delete(usda_ingredient_portion)
    db.session.commit()
    db.session.delete(usda_ingredient)
    db.session.commit()
