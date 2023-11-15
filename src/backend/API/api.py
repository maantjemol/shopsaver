from typing import TypedDict, List
import sqlite3 


def get_taxomony(connection:sqlite3.Connection):
    query = "SELECT * FROM taxomony t"
    cursor = connection.cursor()
    cursor.execute(query)
    return cursor.fetchall()

if __name__ == "__main__":
    connection = sqlite3.connect("../../../database/main.sqlite")
    print(get_taxomony(connection))