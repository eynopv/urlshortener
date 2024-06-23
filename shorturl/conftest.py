import sqlite3
import sys

from .db import Client


def pytest_configure():
    sys._called_from_test = True  # type: ignore
    client = Client()
    client.create_tables()
    con = sqlite3.connect("test.db")
    con.execute(
        """
        INSERT INTO
            shorturls (
                id,
                destination,
                code,
                created_at,
                updated_at
            ) VALUES (
                :id,
                :destination,
                :code,
                :created_at,
                :updated_at
            )
        """,
        {
            "id": 100,
            "destination": "http://example.com/redirected",
            "code": "existant",
            "created_at": 123,
            "updated_at": 321,
        },
    )
    con.commit()


def pytest_unconfigure():
    client = Client()
    client.drop_tables()
    del sys._called_from_test  # type: ignore
