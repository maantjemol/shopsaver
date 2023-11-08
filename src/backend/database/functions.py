from typing import TypedDict, List
import sqlite3

class Item(TypedDict):
    name: str
    store_id: int
    unit: str # "kilo" | "liter" | "stuk" 
    price: int
    url: str 
    taxomonies: List[str] # taxemony ids

class Taxomony(TypedDict):
    id: int
    name: str

class Store(TypedDict):
    id: int
    name: str
    url: str


def initialize_database(path:str, connection:sqlite3.Connection):
    with open(path) as f:
        connection.executescript(f.read())

# TODO: trow error if item already exists or taxemony does not exists
def add_item(item:Item, connection:sqlite3.Connection):
    sql_add_item = "INSERT INTO item (name, store_id, unit, price, url) VALUES (?, ?, ?, ?, ?)"
    sql_add_taxomony = "INSERT INTO item_taxonomy (item_id, taxonomy_id) VALUES (?, ?)"
    cursor = connection.cursor()
    cursor.execute(sql_add_item, (item["name"], item["store_id"], item["unit"], item["price"], item["url"]))
    item_id = cursor.lastrowid
    for taxomony in item["taxomonies"]:
        cursor.execute(sql_add_taxomony, (item_id, taxomony))
    connection.commit()


def add_taxomony(taxomony:Taxomony, connection:sqlite3.Connection):
    sql_add_taxomony = "INSERT INTO taxomony (id, name) VALUES (?, ?)"
    cursor = connection.cursor()
    cursor.execute(sql_add_taxomony, (taxomony["id"], taxomony["name"]))
    connection.commit()

def add_store(store:Store, connection:sqlite3.Connection):
    sql_add_store = "INSERT INTO store (name, url) VALUES (?, ?)"
    cursor = connection.cursor()
    cursor.execute(sql_add_store, (store["name"], store["url"]))
    connection.commit()

def get_items_by_taxomony(taxomony_id:int, connection:sqlite3.Connection):
    query = "SELECT * FROM item LEFT JOIN item_taxonomy ON item_taxonomy.item_id = item.id WHERE item_taxonomy.taxonomy_id = ?"
    cursor = connection.cursor()
    cursor.execute(query, (taxomony_id,))
    return cursor.fetchall()

if __name__ == "__main__":
    connection = sqlite3.connect("../../../database/main.sqlite")
    print(get_items_by_taxomony(8087, connection))