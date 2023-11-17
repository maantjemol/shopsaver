from typing import TypedDict, List
import sqlite3 

# This function makes the connection from this python file to the database. 
def connect_to_db():
    conn = sqlite3.connect('../../../database/main.sqlite')
    return conn

#This function requests a table from the database and stores the data in a python l
def get_Products():
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

# def get_Items():
#     Items = []
#     try:
#         conn = connect_to_db()
#         conn.row_factory = sqlite3.Row
#         cur = conn.cursor()
#         cur.execute("SELECT * FROM item JOIN item_taxomony ON (id=item_id)")
#         rows = cur.fetchall()

#         #This loops rows and stores the row objects to dictionary called Products
#         for i in rows:
#             Item = {}
#             Item["product_id"] = i["id"]
#             Item["name"] = i["name"]
#             Items.append(Item)

#     except:
#         Items = []

#     return Items

def get_Items():
    items = []
    conn = connect_to_db()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("""SELECT *
                FROM item i JOIN item_taxonomy t ON t.item_id = i.id 
                JOIN store s ON i.store_id=s.id""")
    all_rows = cur.fetchall()

    for i in all_rows:
        item = {}
        item["Product_id"] = i["id"]
        item["Taxonomy_id"] = i["taxonomy_id"]
        item["Product_name"] = i["name"]
        item["Store"] = i["store_id"]
        item["Unit"] = i["unit"]
        item["Product_url"] = i["url"]
        items.append(item)

    return items

if __name__ == "__main__":
    # print(get_Products())
    print(get_Items())

#Probleem 1 geen store naam bij ieder product, alleen store_id
#Probleem 2 hij slaat ieder product meerdere keren op in de dictionary 
