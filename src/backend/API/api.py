from math import inf, prod
from typing import TypedDict, List
import sqlite3 
from flask import Flask, request, jsonify #added to top of file
from flask_cors import CORS #added to top of file

def main(taxonomy_list):
    # For testing
    # taxonomy_list = [864, 866, 876]
    taxonomy_list = [864]
    lowest = lowest_price(taxonomy_list)
    return lowest

def connect_to_db():
    # This function makes the connection from this python file to the database. 
    conn = sqlite3.connect('../../../database/main.sqlite')
    return conn

def get_taxonomy():
    #This function requests a table from the database and stores the data in a python dictionary
    Products = []
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM Taxomony")
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
    # This is a function that connects to the database and converts a table into a python dictionary
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
    # This is a function that connects to the database and converts a table into a python dictionary
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
    # This is a function that connects to the database and converts a table into a python dictionary
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
    #  This function matches the taxonomy_id to the item_id and
    #  returns a list that cointains every item that the taxonomy is linked to
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
    # This function calculates the lowest price of each prodect per store
    # The function takes in the list of the taxonomies that it receives from the website
    # It then uses the function match_taxonomy_to_id() to convert those taxomonies to all item id's it is connected to

    lowest = []

    items = get_items()
    stores = get_grocery_store()
    taxonomy_list = Taxonomy_list
    # For testing:
    # taxonomy_list = [864, 866, 876]

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
        # Here is a loop that filters out the cheapest product from each store.                 
        for i in stores:
            x={"Price": inf}
            for product in products: 
                if product["Sales_price"] < x["Price"] and product["Store"] == i["Store_id"]: 
                    x = product
                    x["Store_name"] = i["Store_name"]
                    x["Taxonomy_id"] = taxonomy
                else:
                    continue
            lowest_per_store.append(x)
        lowest.append(lowest_per_store)
            
    return lowest


if __name__ == "__main__":
    print("")
    print(main(10))
