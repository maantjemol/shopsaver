import sqlite3
import database.functions as db
import webscraper.ah as ah
import webscraper.jumbo as jumbo
from filter import getItemTaxonomies, removeBlacklist

if __name__ == "__main__":
    # connection = sqlite3.connect("../../database/main.sqlite")

    # db.initialize_database(connection=connection, path="./database/initialize.sql")
    # data = ah.fetch_data_cache("../../cache/ah.json")
    # taxonomies = ah.parseTaxonomies(data)
    # products = ah.parseProducts(data)

    # for taxomony in taxonomies:
    #     db.add_taxomony(taxomony, connection=connection)

    # for product in products:
    #     db.add_item(product, connection=connection)

    connection = sqlite3.connect("../../database/main.sqlite")
    allItems = db.get_all_taxomonies_with_items(connection)
    
    items = jumbo.fetch_data_cache("../../cache/jumbo.json")
    products = jumbo.parseProducts(items)

    for product in products:
        jumboTax = getItemTaxonomies(product, allItems)
        print(product["name"])
    
        taxss = []
        for tax in jumboTax:
            taxss.append( db.get_taxomony_by_id(tax, connection))
        
        for tax in taxss:
            print(" ", tax["name"])
