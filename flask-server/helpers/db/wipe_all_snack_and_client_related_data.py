from flask_sqlalchemy import SQLAlchemy
from models import (
    Snack_Model,
    Meal_Plan_Snack_Model,
    Scheduled_Order_Snack_Model,
    Schedule_Snack_Model,
)


def wipe_all_snack_and_client_related_data(db: SQLAlchemy) -> None:
    snacks = db.session.query(Snack_Model).all()
    meal_plan_snacks = db.session.query(Meal_Plan_Snack_Model).all()
    for snack in snacks:
        associated_scheduled_order_snacks = (
            db.session.query(Scheduled_Order_Snack_Model)
            .filter(Scheduled_Order_Snack_Model.snack_id == snack.id)
            .all()
        )
        for scheduled_order_snack in associated_scheduled_order_snacks:
            db.session.delete(scheduled_order_snack)

        associated_schedule_snacks = (
            db.session.query(Schedule_Snack_Model)
            .filter(Schedule_Snack_Model.snack_id == snack.id)
            .all()
        )
        for schedule_snack in associated_schedule_snacks:
            db.session.delete(schedule_snack)

    for meal_plan_snack in meal_plan_snacks:
        for recipe_ingredient in meal_plan_snack.recipe:
            for recipe_ingredient_nutrient in recipe_ingredient.nutrients:
                db.session.delete(recipe_ingredient_nutrient)
            db.session.delete(recipe_ingredient)
        db.session.delete(meal_plan_snack)
    for snack in snacks:
        db.session.delete(snack)
    db.session.commit()
