from flask_sqlalchemy import SQLAlchemy


class Base_Repository(object):
    def __init__(self, db: SQLAlchemy) -> None:
        self.db: SQLAlchemy = db
