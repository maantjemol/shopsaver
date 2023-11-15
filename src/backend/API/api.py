from typing import TypedDict, List
import sqlite3 


# 
def connect_to_db():
    conn = sqlite3.connect('../../../database/main.sqlite')
    return conn

def get_Products():
    Products = []
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM Taxomony")
        rows = cur.fetchall()

        # convert row objects to dictionary
        for i in rows:
            Product = {}
            Product["id"] = i["id"]
            Product["name"] = i["name"]
            Products.append(Product)

    except:
        Product = []

    return Products


def get_user_by_id(user_id):
    user = {}
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE user_id = ?", 
                       (user_id,))
        row = cur.fetchone()

        # convert row object to dictionary
        user["user_id"] = row["user_id"]
        user["name"] = row["name"]
        user["email"] = row["email"]
        user["phone"] = row["phone"]
        user["address"] = row["address"]
        user["country"] = row["country"]
    except:
        user = {}

    return user

def get_taxomony(connection:sqlite3.Connection):
    query = "SELECT * FROM taxomony"
    cursor = connection.cursor()
    cursor.execute(query)
    return cursor.fetchall()

if __name__ == "__main__":
    # print(get_taxomony(connect_to_db()))
    print(get_Products())