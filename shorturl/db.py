import sqlite3
import time
import string
import random
import sys

from .schemas import NewShortUrl, ShortUrl


class Client:

    def __init__(self):
        if hasattr(sys, "_called_from_test"):
            self.db = "test.db"
        else:
            self.db = "shorturl.db"

    def create_tables(self):
        con = sqlite3.connect(self.db)
        con.execute(
            """
            CREATE TABLE IF NOT EXISTS shorturls(
                id INTEGER PRIMARY KEY,
                destination TEXT NOT NULL,
                code TEXT NOT NULL,
                created_at INTEGER NOT NULL,
                updated_at INTEGER NOT NULL
            )
            """
        )
        con.commit()
        con.close()

    def drop_tables(self):
        con = sqlite3.connect(self.db)
        con.execute("DROP TABLE shorturls")
        con.commit()
        con.close()

    def create_shorturl(self, params: NewShortUrl) -> ShortUrl:
        timestamp = int(time.time())

        con = sqlite3.connect(self.db)
        code = generate_code()

        while True:
            cur = con.execute("SELECT 1 FROM shorturls WHERE code = ?", [code])
            result = cur.fetchone()
            if not result:
                break
            code = generate_code()

        short_url = ShortUrl(
            destination=params.destination,
            code=code,
            created_at=timestamp,
            updated_at=timestamp,
        )
        cur = con.execute(
            """
                          INSERT INTO
                            shorturls(
                                destination,
                                code,
                                created_at,
                                updated_at
                            )
                          VALUES (
                              :destination,
                              :code,
                              :created_at,
                              :updated_at
                            )
                          RETURNING id
                          """,
            {
                "destination": params.destination,
                "code": code,
                "created_at": timestamp,
                "updated_at": timestamp,
            },
        )
        ids = cur.fetchone()
        con.commit()
        con.close()
        short_url.id = ids[0]
        return short_url

    def get_shorturl_by_code(self, code: str) -> ShortUrl | None:
        con = sqlite3.connect(self.db)
        cur = con.execute(
            "SELECT id, destination, code, created_at, updated_at FROM shorturls WHERE code = ?",
            [code],
        )
        shorturl = cur.fetchone()
        con.close()

        if not shorturl:
            return None

        return ShortUrl(
            id=shorturl[0],
            destination=shorturl[1],
            code=shorturl[2],
            created_at=shorturl[3],
            updated_at=shorturl[4],
        )


def generate_code(length: int = 6) -> str:
    characters = string.ascii_letters + string.digits
    short_url = "".join(random.choice(characters) for _ in range(length))
    return short_url
