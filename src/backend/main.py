import sqlite3
from product_processor import process_product
import database.functions as db
import webscraper.ah as ah
import webscraper.jumbo as jumbo
from filter import getItemTaxonomies, removeBlacklist
from multiprocessing import Pool

if __name__ == "__main__":
    connection = sqlite3.connect("../../database/main.sqlite")

    db.initialize_database(connection=connection, path="./database/initialize.sql")
    data = ah.fetch_data_cache("../../cache/ah.json")
    taxonomies = ah.parseTaxonomies(data)
    products = ah.parseProducts(data)

    for taxomony in taxonomies:
        db.add_taxomony(taxomony, connection=connection)

    # print progress
    for i in range(len(products)):
        print("progress: " + str(i) + "/" + str(len(products)))
        db.add_item(products[i], connection=connection)
    connection.commit()

    allItems = db.get_all_taxomonies_with_items(connection)
    
    items = jumbo.fetch_data_cache("../../cache/jumbo.json")
    products = jumbo.parseProducts(items)

    # for i in range(len(products)):
    #     product = products[i]
    #     jumboTax = getItemTaxonomies(product, allItems)
    #     # print progress 
    #     print("progress: " + str(i) + "/" + str(len(products)))
    #     product["taxomonies"] = jumboTax
    #     db.add_item(product, connection=connection)
    
    with Pool() as p:
        p.starmap(process_product, [(i, products, allItems) for i in range(len(products))])
