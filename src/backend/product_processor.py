import sqlite3
from filter import getItemTaxonomies
import database.functions as db

def process_product(i, products, allItems):
    connection = sqlite3.connect("../../database/main.sqlite")
    product = products[i]
    jumboTax = getItemTaxonomies(product, allItems)
    print("progress: " + str(i) + "/" + str(len(products)))
    product["taxomonies"] = jumboTax
    db.add_item(product, connection=connection)
    connection.commit()
    connection.close()
