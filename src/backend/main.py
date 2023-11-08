import sqlite3
import database.functions as db
import webscraper.ah as ah


if __name__ == "__main__":
    connection = sqlite3.connect("../../database/main.sqlite")

    db.initialize_database(connection=connection, path="./database/initialize.sql")
    data = ah.fetch_data_cache("../../cache/ah.json")
    taxonomies = ah.parseTaxonomies(data)
    products = ah.parseProducts(data)

    for taxomony in taxonomies:
        db.add_taxomony(taxomony, connection=connection)

    for product in products:
        db.add_item(product, connection=connection)
    
