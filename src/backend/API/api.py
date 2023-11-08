from typing import TypedDict, List
import sqlite3 
# import os.path

# BASE_DIR = os.path.dirname(os.path.abspath(SHOPSAVER))
# db_path = os.path.join(BASE_DIR, "main.sqlite")
# with sqlite3.connect(db_path) as db:


def get_taxomony(connection:sqlite3.Connection):
    query = "SELECT name FROM taxomony t"
    cursor = connection.cursor()
    cursor.execute(query)
    return cursor.fetchall()

if __name__ == "__main__":
    connection = sqlite3.connect("../../../database/main.sqlite")
    print(get_taxomony(connection))