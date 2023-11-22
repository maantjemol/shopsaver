import json
import os
import sqlite3
from product_processor import process_product
import database.functions as db
import webscraper.ah as ah
import webscraper.jumbo as jumbo
import webscraper.hoogvliet as hoogvliet
from filter import getItemTaxonomies, removeBlacklist
from multiprocessing import Pool

def update_from_cache():
    """
    First the database is deleted, than a new connection is made (a new database). 
    This database will be filled with the data from the supermarkets, where multithreading is used to 

    Returns:
    Nothing
    """
    # delete database file:
    os.remove("../../database/main.sqlite")
    
    connection = sqlite3.connect("../../database/main.sqlite")


    # AH
    db.initialize_database(connection=connection, path="./database/initialize.sql")
    data = ah.fetch_data_cache("../../cache/ah.json")
    taxonomies = ah.parseTaxonomies(data)
    products = ah.parseProducts(data)

    for taxomony in taxonomies:
        db.add_taxomony(taxomony, connection=connection)

    for i in range(len(products)):
        print("progress: " + str(i) + "/" + str(len(products)))
        db.add_item(products[i], connection=connection)
    connection.commit()

    # Jumbo
    allItems = db.get_all_taxomonies_with_items(connection)
    
    items = jumbo.fetch_data_cache("../../cache/jumbo.json")
    products = jumbo.parseProducts(items)

    with Pool() as p:
        p.starmap(process_product, [(i, products, allItems) for i in range(len(products))])

    # Hoogvliet
    items = hoogvliet.fetch_data_cache("../../cache/hoogvliet.json")
    products = hoogvliet.parseProducts(items)

    with Pool() as p:
        p.starmap(process_product, [(i, products, allItems) for i in range(len(products))])


if __name__ == "__main__":
    update_from_cache()