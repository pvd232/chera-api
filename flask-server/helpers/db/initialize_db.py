from sqlalchemy.engine import Engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import MetaData


def initialize_db(db_engine: Engine, drop_tables: bool) -> None:
    meta = MetaData()
    meta.reflect(bind=db_engine)
    Base = declarative_base()
    Base.metadata = meta
    if drop_tables:
        Base.metadata.drop_all(db_engine)
    Base.metadata.create_all(db_engine)
