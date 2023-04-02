# To create a single table with SQLAlchemy, you need to first import the necessary modules and create a database engine. After that, define the table structure using SQLAlchemy's `Table` and `Column` classes, and then create the table using the `create_all()` method of the database engine object.

# Here's an example code that creates a single table called `users` with 3 columns (`id`, `name`, and `email`):

from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData


def create_recipe_ingredient_nutrient_table(database_url: str) -> None:
    engine = create_engine(database_url, echo=True)

    metadata = MetaData()

    recipe_ingredient_nutrients = Table('recipe_ingredient_nutrient', metadata,
                                        Column('id', Integer,
                                               primary_key=True),
                                        Column('name', String),
                                        Column('email', String)
                                        )

    metadata.create_all(engine)


# In this example, we are using an SQLite database and storing it in a file called `example.db`. The `echo=True` argument is optional and enables logging of SQL statements. You can replace the database URL with one that corresponds to your chosen database system (MySQL, PostgreSQL, etc).

# The `Table` and `Column` classes are used to define the table structure. The `metadata` object is used to hold references to all the defined tables, and is passed as an argument to the `create_all()` method, which creates all the defined tables in the database.

# Note that the `create_all()` method is idempotent, so running it multiple times will not create duplicate tables.
