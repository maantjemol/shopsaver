import sqlite3
from filter import getItemTaxonomies
import database.functions as db

def process_product(i, products, allItems):
    """
    Initiate a connection with the database and select a product from the list of products we scraped from the supermarket's website.
    We execute getItemTaxomonies for each product and add the product to the database. 
    The function also prints a indication of the progress. 

    Parameters:
    i: an integer iterating over the elements of the products-list
    products: List of items (products)
    allItems: a List of Dictionaries describing all items and their taxomony's

    Returns:
    Nothing
    """
    connection = sqlite3.connect("../../database/main.sqlite")
    product = products[i]
    jumboTax = getItemTaxonomies(product, allItems)
    print("progress: " + str(i) + "/" + str(len(products)))
    product["taxomonies"] = jumboTax
    db.add_item(product, connection=connection)
    connection.commit()
    connection.close()
