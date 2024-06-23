from .db import Client

if __name__ == "__main__":
    client = Client()
    client.create_tables()
