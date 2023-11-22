from typing import TypedDict, List
import sqlite3

class Item(TypedDict):
    name: str
    store_id: int
    unit: str # "kilo" | "liter" | "stuk" 
    price: int
    url: str 
    taxomonies: List[str] # taxemony ids
    sales_price: int

class Taxomony(TypedDict):
    id: int
    name: str

class Store(TypedDict):
    id: int
    name: str
    url: str


def initialize_database(path:str, connection:sqlite3.Connection):
    """
    Initializes the database with tables by executing the script of a file.
    
    Parameters: 
    path (str): Path towards a file
    connection (sqlite3 object): 

    Returns:
    Nothing
    
    Praktisch: 
    Dmv path (linkje naar initialize.sql) kunnen we in main de database opzetten. 
    Initialize.sql is een SQL bestand waar we de tabellen creëren. 


    """
    with open(path) as f:
        connection.executescript(f.read())

def add_item(item:Item, connection:sqlite3.Connection):
    """
    Format the Items to SQL commands and execute the commands. 
    Extract the values of the characteristics from an item and format the SQL command to insert the item into the database. 
    
    Parameters:
    item:(Item): Dictionary with characteristics of an item.
    connection (sqlite3 object): 
    
    Returns:
    Nothing
    """
    sql_add_item = "INSERT INTO item (name, store_id, unit, price, url, sales_price) VALUES (?, ?, ?, ?, ?, ?)"
    sql_add_taxomony = "INSERT INTO item_taxonomy (item_id, taxonomy_id) VALUES (?, ?)"
    cursor = connection.cursor()
    cursor.execute(sql_add_item, (item["name"], item["store_id"], item["unit"], item["price"], item["url"], item["sales_price"]))
    item_id = cursor.lastrowid
    for taxomony in item["taxomonies"]:
        cursor.execute(sql_add_taxomony, (item_id, taxomony))
    connection.commit()


def add_taxomony(taxomony:Taxomony, connection:sqlite3.Connection):
    """
    Format the taxomony to SQL commands and execute the commands. 
    Extract the values of the characteristics from a taxomony and format the SQL command to insert the item into the database. 
    
    Parameters:
    taxomony:(Taxomony): Dictionary with characteristics of a taxomony.
    connection (sqlite3 object): 
    
    Returns:
    Nothing
    """
    sql_add_taxomony = "INSERT INTO taxomony (id, name) VALUES (?, ?)"
    cursor = connection.cursor()
    cursor.execute(sql_add_taxomony, (taxomony["id"], taxomony["name"]))
    connection.commit()

def add_store(store:Store, connection:sqlite3.Connection):
    """
    Format the taxomony to SQL commands and execute the commands. 
    Extract the values of the characteristics from a store and format the SQL command to insert the item into the database. 
    
    Parameters:
    store:(Store): Dictionary with characteristics of a store.
    connection (sqlite3 object): 
    
    Returns:
    Nothing
    """
    sql_add_store = "INSERT INTO store (name, url) VALUES (?, ?)"
    cursor = connection.cursor()
    cursor.execute(sql_add_store, (store["name"], store["url"]))
    connection.commit()

def get_items_by_taxomony(taxomony_id:int, connection:sqlite3.Connection):
    """
    Perform a SQL query to select all item id's belonging to a certain taxonomy.
    We do this by using a left join on the tables item and item_taxonomy, where we join on the item_id's. 

    Preconditions:
    taxonomy_id: int with a value > 0
    
    Parameters: 
    taxomony_id(int):  Integer matched with a certain taxemony name (for example: 1641, "Aardappel, groente, fruit")
    connection (sqlite3 object): 

    Returns:
    A List of Dictionaries describing items. 
    """

    query = "SELECT * FROM item LEFT JOIN item_taxonomy ON item_taxonomy.item_id = item.id WHERE item_taxonomy.taxonomy_id = ?"
    cursor = connection.cursor()
    cursor.execute(query, (taxomony_id,))
    response = cursor.fetchall()
    products = []
    for item in response:
        products.append({
            "name": item[1],
            "store_id": item[2],
            "unit": item[3],
            "price": item[4],
            "url": item[5],
            "taxomonies": [item[-1]]
        })
    return products

def get_all_taxomonies_with_items(connection:sqlite3.Connection):
    """"
    Perform a SQL query to select all taxonomy id's belonging to an item, for all items in the table.
    
    Parameters: 
    connections (sqlite3 object): 

    Returns:
    returns a List of Dictionaries describing all items and their taxomony's
    """"
    
    query = "SELECT id FROM taxomony t"
    cursor = connection.cursor()
    cursor.execute(query)
    response = cursor.fetchall()
    data = []
    for taxomony in response:
        items:List[Item] = get_items_by_taxomony(taxomony[0], connection)
        data.append({
            "id": taxomony[0],
            "items": items
        })
    return data

def get_taxomony_by_id(taxomony_id:int, connection:sqlite3.Connection):
    """""
    Perform a SQL query to retrieve the taxonomy name using the taxonomy id. 

    Preconditions:
    taxonomy_id: int with a value > 0
    
    Parameters: 
    taxomony_id(int): Integer matched with a certain taxemony name
    
    Returrns:
    The taxonomy id with its name.
    """"
    query = "SELECT * FROM taxomony WHERE id = ?"
    cursor = connection.cursor()
    cursor.execute(query, (taxomony_id,))
    response = cursor.fetchone()
    return {
        "id": response[0],
        "name": response[1]
    }

if __name__ == "__main__":
    connection = sqlite3.connect("../../../database/main.sqlite")
    response = get_items_by_taxomony(4979, connection)
    print(response)