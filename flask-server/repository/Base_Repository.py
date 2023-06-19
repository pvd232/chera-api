from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
from .Base_DB import Base_DB


class Base_Repository(object):
    def __init__(self, db: SQLAlchemy = None, engine=None) -> None:
        if db:
            self.db: SQLAlchemy = db
        # This allows testing using an engine associated with a different database
        else:
            Session = sqlalchemy.orm.sessionmaker(bind=engine)
            session = Session()
            self.db = Base_DB(session=session)
