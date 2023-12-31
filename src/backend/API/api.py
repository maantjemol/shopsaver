from math import inf, prod
from typing import TypedDict, List
import sqlite3 


def main(taxonomy_list):
    '''
    This is the main function that runs all the code and we use for testing

    Parameters: 
    taxonomy_list: A list that contains all taxonomy ID's from products the user selected.

    Returns: 
    A list that contains the cheapest products for each store.

    '''
    # For testing
    # taxonomy_list = [864, 866, 876]
    taxonomy_list = [864]

    lowest = lowest_price(taxonomy_list)
    return lowest

def connect_to_db():
    '''
    This function makes the connection from this python file to the database and is used to shorten the code when 
    writing functions that need to receive tables from the database.

    Returns: a variable conn that is a connection to our database file. 

    '''
    conn = sqlite3.connect('../../../database/main.sqlite')
    return conn

def get_taxonomy():
    '''
    This function requests the taxonomy table from the database and stores the data in a python dictionary
    
    Returns: 
    A list of dictionaries that contains all the products within the taxonomy table.
    '''
    Products = []
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT t.id, t.name FROM taxomony t WHERE NOT EXISTS (SELECT s.id FROM store s WHERE NOT EXISTS ( SELECT i.id FROM item_taxonomy it JOIN item i ON it.item_id = i.id WHERE it.taxonomy_id = t.id AND i.store_id = s.id));")
        rows = cur.fetchall()

        #This loops rows and stores the row objects to dictionary called Products
        for i in rows:
            Product = {}
            Product["product_id"] = i["id"]
            Product["name"] = i["name"]
            Products.append(Product)

    except:
        Products = []

    return Products

def get_items():            
    '''
    This is a function that connects to the database and converts the item table into a python dictionary

    Returns: 
    A list of dictionaries that cointains the information of every item within the item table stored in 
    the database. 
    '''
    items = []
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("""SELECT *
                    FROM item  
                    """)
        all_rows = cur.fetchall()
        for i in all_rows:
            item = {}
            item["Product_id"] = i["id"]
            item["Product_name"] = i["name"]
            item["Store"] = i["store_id"]
            item["Unit"] = i["unit"]
            item["Price"] = i["price"]
            item["Product_url"] = i["url"]
            item["Sales_price"] = i["sales_price"]
            items.append(item)
        
    except:
        items = []

    return items

def get_taxonomy_id():
    '''
    This is a function that connects to the database and converts the taxonomy_id table into a python dictionary
    
    Returns: 
    A list of dictionaries that cointains the information from the item_taxonomy table. 
    '''
    taxonomy_id = []
    try: 
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM item_taxonomy")
        rows = cur.fetchall()

        #This loops rows and stores the row objects to dictionary called Products
        for i in rows:
            taxonomy = {}
            taxonomy["Product_id"] = i["item_id"]
            taxonomy["Taxonomy_id"] = i["taxonomy_id"]
            taxonomy_id.append(taxonomy)
    except:
        taxonomy_id = []

    return taxonomy_id

def get_grocery_store():
    '''
    This is a function that connects to the database and converts the stores table into a python dictionary
    
    Returns:
    A list of dictionaries that cointains the information from the store table.
    '''
    grocery_store = []
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM store")
        rows = cur.fetchall()

        for i in rows:
            grocery = {}
            grocery["Store_id"] = i["id"]
            grocery["Store_name"] = i["name"]
            grocery_store.append(grocery)

    except:
        grocery_store = []

    return grocery_store

def match_taxonomy_to_id(Taxonomy):
    '''
    This function matches the taxonomy_id to the item_id and
     returns a list that cointains every item that the taxonomy is linked to
    
    Parameter: 
    Taxonomy: a integer value that represents the taxonomy id.

    Returns: 
    A list of products ID's that are linked to the taxonomy
    '''
    Matches = []
    taxonomy = Taxonomy
    # For testing
    # taxonomy = 864
    ids = get_taxonomy_id()
    for id in ids: 
        if id["Taxonomy_id"] == taxonomy:
            Matches.append(id["Product_id"])
        else:
            continue
    return Matches

def lowest_price(Taxonomy_list):
    '''
    This function calculates the lowest price of each prodect per store

    Parameter:
    Taxonomy_list: a list of the taxonomies that it receives from the website that were selected by the user
    
    Returns: 
    A list of dictionaries that cointains the lowest price per product for each store. 
    '''

    lowest = []

    items = get_items()
    stores = get_grocery_store()
    taxonomy_list = Taxonomy_list
    # For testing:
    # taxonomy_list = [864, 866, 876]

    # This loop creates a dictionary for each store which we will later append the lowest product to
    for i in stores:
        lowest.append({"Store_name": i["Store_name"], "Store_id": i["Store_id"], "products": []})

    # First for loop that selects the first taxonomy and converts it the product Id's 
    for taxonomy in taxonomy_list:
        lowest_per_store = []
        
        products = []
        store_id = []

        Products_ID = match_taxonomy_to_id(taxonomy)
        # Since a taxonomy is usually linked to multiple item/product Id's we loop over eacht new product ID we got
        # Note that product_id and item_id are the same, where product_id refers to our selected products and 
        # item id refers to the items in the database 
        for ID in Products_ID:
            for item in items:         
                if ID == item["Product_id"]:
                    products.append(item)
                    if item["Store"] not in store_id:
                        store_id.append(item["Store"])
                else:
                    continue   
        # Here is a loop that filters out the cheapest product from each store and appends it to the correct dictionary 
        # created earlier.                 
        for i in range(len(lowest)):
            x={"Price": inf}
            store = lowest[i]
            for product in products: 
                if product["Sales_price"] < x["Price"] and product["Store"] == store["Store_id"]: 
                    x = product
                    x["Taxonomy_id"] = taxonomy
                else:
                    continue
            lowest[i]["products"].append(x)
            
    return lowest


def get_join_table():
    '''
    This is a function that connects to the database and joins the
    item_taxonomy table to the item table and converts the table into a python dictionary

    Returns: 
    A list of dictionaries that contains every match between product_id, store_id and item_id
    '''
    all_id = []
    try: 
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM item_taxonomy it JOIN item i ON(it.item_id = i.id)")
        rows = cur.fetchall()

        #This loops rows and stores the row objects to dictionary called Products
        for i in rows:
            taxonomy = {}
            taxonomy["Store_id"] = i["store_id"]
            taxonomy["Taxonomy_id"] = i["taxonomy_id"]
            taxonomy["Item_id"] = i["id"]
            all_id.append(taxonomy)
        
    except:
        all_id = []

    return all_id


def filtered_taxonomies():
    '''
    This function filters out the taxomonies that do not belong to products that are sold in every store
    
    Returns: 
    A list of dictionaries that contains every taxonomy id that matches with an item that is sold in every store
    '''
    filtered = []
    

    taxonomies = get_taxonomy()
    all_id = get_join_table()
    stores = get_grocery_store()

    # This loop stores all the store_id values 
    store_id = []
    for store in stores:
        store_id.append(store["Store_id"])

    # This loops over every taxonomy and tries to match it with every item that is linked to the taxonomy
    # and stores the value of every store_id inside in_store, once in_store is equal to store_id we know it is sold in every
    # store.
    for taxonomy in taxonomies: 
        in_store = []
        for id in all_id:
            if taxonomy["product_id"] == id["Taxonomy_id"] and id["Store_id"] not in in_store:
                in_store.append(id["Store_id"])
                if in_store == store_id:
                    break
        if in_store == store_id:
            filtered.append(taxonomy)
    
    return filtered


if __name__ == "__main__":
    print("")
    # print(main(10))
    # print(get_filter())
    print(main([209]))

    
