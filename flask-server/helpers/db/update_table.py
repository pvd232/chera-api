from sqlalchemy import (
    Table,
    Column,
    Integer,
    Float,
    String,
    Boolean,
    ForeignKey,
    ForeignKeyConstraint,
    MetaData,
    CheckConstraint,
    UUID,
    create_engine,
)


def update_table(database_url: str, query: str) -> None:
    # TODO update with this https://www.geeksforgeeks.org/python-sqlalchemy-update-table-structure/
    # create engine
    engine = create_engine(database_url)
    connection = engine.connect()
    connection.execute(query)
