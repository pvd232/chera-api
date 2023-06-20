from flask_sqlalchemy import SQLAlchemy
from uuid import UUID
from models import Meal_Model, Meal_Plan_Meal_Model


def wipe_meal_data(db: SQLAlchemy, meal_id: UUID) -> None:
    meal = db.session.query(Meal_Model).filter(Meal_Model.id == meal_id).first()
    if meal:
        meal_plan_meals = (
            db.session.query(Meal_Plan_Meal_Model)
            .filter(Meal_Plan_Meal_Model.meal_id == meal_id)
            .all()
        )
        for meal_plan_meal in meal_plan_meals:
            for recipe_ingredient in meal_plan_meal.recipe:
                for recipe_ingredient_nutrient in recipe_ingredient.nutrients:
                    db.session.delete(recipe_ingredient_nutrient)
                db.session.delete(recipe_ingredient)
            db.session.delete(meal_plan_meal)
        for meal_dietary_restriction in meal.dietary_restrictions:
            db.session.delete(meal_dietary_restriction)
        db.session.delete(meal)
        db.session.commit()
