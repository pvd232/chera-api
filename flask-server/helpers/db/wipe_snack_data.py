from flask_sqlalchemy import SQLAlchemy
from uuid import UUID
from models import Snack_Model, Meal_Plan_Snack_Model


def wipe_snack_data(db: SQLAlchemy, snack_id: UUID) -> None:
    snack = db.session.query(Snack_Model).filter(Snack_Model.id == snack_id).first()
    if snack:
        snack_plan_snacks = (
            db.session.query(Meal_Plan_Snack_Model)
            .filter(Meal_Plan_Snack_Model.snack_id == snack_id)
            .all()
        )
        for snack_plan_snack in snack_plan_snacks:
            for recipe_ingredient in snack_plan_snack.recipe:
                for recipe_ingredient_nutrient in recipe_ingredient.nutrients:
                    db.session.delete(recipe_ingredient_nutrient)
                db.session.delete(recipe_ingredient)
            db.session.delete(snack_plan_snack)
        db.session.delete(snack)
        db.session.commit()
