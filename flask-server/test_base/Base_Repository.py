import unittest
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from models import connection_string


engine = create_engine(connection_string, pool_size=100, max_overflow=10)


class Base_Repository(unittest.TestCase):
    def __init__(self):
        super().__init__()
        load_dotenv()

        # connect to the database
        self.connection = engine.connect()

        # begin a non-ORM transaction
        self.trans = self.connection.begin()

        # bind an individual Session to the connection, selecting
        # "create_savepoint" join_transaction_mode
        self.session = Session(
            bind=self.connection, join_transaction_mode="create_savepoint"
        )

    def tearDown(self):
        self.session.close()

        # rollback - everything that happened with the
        # Session above (including calls to commit())
        # is rolled back.
        self.trans.rollback()

        # return connection to the Engine
        self.connection.close()

    # def test_query_panel(self):
    #     expected = [self.panel]
    #     result = self.session.query(Panel).all()
    #     self.assertEqual(result, expected)
