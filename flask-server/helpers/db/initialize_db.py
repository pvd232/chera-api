from sqlalchemy.engine import Engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import MetaData


def initialize_db(
    source_db_engine: Engine, target_db_engine: Engine, drop_tables: bool
) -> None:
    meta = MetaData()
    meta.reflect(bind=source_db_engine)
    Base = declarative_base()
    Base.metadata = meta
    if drop_tables:
        Base.metadata.drop_all(target_db_engine)
    Base.metadata.create_all(target_db_engine)
