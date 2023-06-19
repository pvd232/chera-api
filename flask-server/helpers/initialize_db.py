from flask_sqlalchemy import SQLAlchemy


def initialize_db(db: SQLAlchemy, drop_tables: bool) -> None:
    if drop_tables:
        db.drop_all()
    db.create_all()
