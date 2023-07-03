import sqlite3
import click
import os


def get_db():
    # Establishes connection to database
    path = os.getcwd()
    # path = os.path.join(path, os.pardir) # api directory
    # db_path = os.path.abspath(os.path.join(path, os.pardir, "db"))
    db_path = os.path.abspath(os.path.join(path, "db"))
    
    # Check if db path exists. If not, make it
    if not os.path.exists(db_path):
        os.makedirs(db_path)
    
    db = sqlite3.connect(
        # Create sqlite3 db instance in adjacent directory
        os.path.join(db_path, "users.sqlite"),
        detect_types=sqlite3.PARSE_DECLTYPES
    )
    db.row_factory = sqlite3.Row
    return db


def init_db():
    db = get_db()
    schema = os.path.join("api", "db", "schema.sql")
    with open(schema, "r") as f:
        db.executescript(f.read())


if __name__ == "__main__":
    init_db()