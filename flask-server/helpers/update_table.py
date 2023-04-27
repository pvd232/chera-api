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


def update_table(database_url: str, table_name: str) -> None:
    # create engine
    engine = create_engine(database_url)

    # create metadata object
    metadata = MetaData()

    # Define a table with foreign key constraint
    # reflect existing tables
    metadata.reflect(bind=engine)

    my_table = Table(table_name, metadata, autoload_with=engine)
    # table = Table(
    #     "recipe_ingredient",
    #     metadata,
    #     Column("id", UUID(as_uuid=True), primary_key=True, unique=True, nullable=False),
    #     Column(
    #         "usda_ingredient_id",
    #         String(80),
    #         ForeignKey("usda_ingredient.id"),
    #         primary_key=True,
    #         nullable=False,
    #     ),
    #     Column(
    #         "meal_plan_meal_id",
    #         UUID(as_uuid=True),
    #         ForeignKey("meal_plan_meal.id"),
    #         nullable=True,
    #     ),
    #     Column(
    #         "meal_plan_snack_id",
    #         UUID(as_uuid=True),
    #         ForeignKey("meal_plan_snack.id"),
    #         nullable=True,
    #     ),
    #     Column(
    #         "usda_ingredient_portion_id",
    #         UUID(as_uuid=True),
    #         ForeignKey("usda_ingredient_portion.id"),
    #         nullable=False,
    #     ),
    #     Column("quantity", Float, nullable=False),
    #     Column("active", Boolean, default=True, nullable=False),
    # )

    # Update the foreign key constraint to reference the new column
    table_fk = ForeignKeyConstraint(
        ["meal_plan_snack_id"], ["meal_plan_snack.id"], name="fk_meal_plan_snack_id"
    )
    my_table.append_constraint(table_fk)

    # Update the table schema in the database
    my_table.update()
